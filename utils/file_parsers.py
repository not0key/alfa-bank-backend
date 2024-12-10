from docx import Document
import docx


def extract_sections_from_docx(file_path, sections) -> dict:
    """
    Извлекает текст между указанными разделами документа DOCX.

    :param file_path: Путь к файлу DOCX
    :param start_section: Название начального раздела
    :param end_section: Название конечного раздела
    :return: Список строк с содержимым между начальным и конечным разделами
    """

    def extract_content_between_points(file_path, sections):
        doc = Document(file_path)
        all_sections = []  # Массив для хранения всех разделов
        current_section = []  # Массив для текущего раздела
        inside_range = False  # Флаг, указывающий, находимся ли мы в диапазоне

        # Проход по всем элементам документа
        for element in doc.element.body:
            if element.tag.endswith('p'):  # Если это параграф
                paragraph = element.text.strip()
                if not paragraph:  # Пропускаем пустые строки
                    continue

                for start_point, end_point in sections:
                    # Если мы находим начало раздела и не в диапазоне предыдущего
                    if paragraph.startswith(start_point):
                        if current_section:  # Если в текущем разделе есть данные, добавляем их в общий список
                            all_sections.append(current_section)
                        current_section = []  # Очищаем текущий раздел
                        inside_range = True
                        continue

                    # Если мы находим конец раздела и находимся внутри диапазона
                    if paragraph.startswith(end_point) and inside_range:
                        inside_range = False
                        # last_end = end_point  # Обновляем последний конец
                        # break

                # Добавляем параграф в текущий раздел, если внутри диапазона
                if inside_range:
                    current_section.append({'type': 'text', 'content': paragraph})

            elif element.tag.endswith('tbl') and inside_range:  # Если это таблица и внутри диапазона
                table = []
                for row in element.findall(".//w:tr", namespaces=doc.element.nsmap):
                    cells = []
                    for cell in row.findall(".//w:tc", namespaces=doc.element.nsmap):
                        # Собираем весь текст внутри ячейки
                        cell_text = ""
                        for text in cell.findall(".//w:t", namespaces=doc.element.nsmap):
                            if text.text:
                                cell_text += text.text.strip()  # Добавляем текст ячейки
                        cells.append(cell_text)  # Добавляем текст ячейки в список
                    table.append(cells)  # Добавляем строку таблицы в таблицу
                current_section.append({'type': 'table', 'content': table})

            # Пропускаем изображения
            if 'drawing' in element.tag:
                continue

        # Добавляем последний раздел, если он был
        if current_section:
            all_sections.append(current_section)

        return all_sections

    all_content = extract_content_between_points(file_path, sections)
    sections_dict = {}

    # Перебираем все разделы
    for section_index, section in enumerate(all_content):
        section_name = ""
        section_content = []  # Содержимое текущей секции

        # Перебираем элементы внутри раздела
        for item_index, item in enumerate(section):
            if item_index == 0:  # Если это название раздела
                section_name = item['content']
            elif item['type'] == 'table':  # Если это таблица
                table_content = "\n".join(["\t".join(row) for row in item['content']])
                section_content.append(f"Таблица:\n{table_content}")
            elif item['type'] == 'text':  # Если это текст
                section_content.append(f"Текст: {item['content']}")

        # Добавляем раздел с содержимым в итоговый словарь
        sections_dict[section_name] = section_content

    return sections_dict
