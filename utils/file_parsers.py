from docx import Document


def extract_sections_from_docx(file_path: str, start_section: str, end_section: str, sections : list) -> dict:
    """
    Извлекает текст между указанными разделами документа DOCX.

    :param file_path: Путь к файлу DOCX
    :param start_section: Название начального раздела
    :param end_section: Название конечного раздела
    :return: Список строк с содержимым между начальным и конечным разделами
    """
    document = Document(file_path)
    result = {}
    is_within_section = False  # Флаг для определения текущего раздела
    section = ""
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        # Если текст совпадает с начальным разделом, начинаем извлечение
        """if text.lower().startswith(start_section.lower()):
            is_within_section = True"""
        for s in sections:
            if text.lower().startswith(s.lower()):
                section = s
                break

        # Если текст совпадает с конечным разделом, завершаем извлечение
        if is_within_section and text.startswith(end_section):
            is_within_section = False
            section = ""

        if section != "":
            if section not in result:
                result[section] = []
            result[section].append(text)

        # Сохраняем текст, если мы находимся в целевом разделе
        # if is_within_section:
        #     result.append(text)

    return result
