from pathlib import Path
from utils.file_parsers import extract_sections_from_docx

TEMP_DIR = Path("temp")  # Директория для временных файлов
TEMP_DIR.mkdir(exist_ok=True)  # Убедимся, что папка существует


async def process_uploaded_file(file) -> list:
    """
    Обрабатывает загруженный файл: сохраняет временно, парсит, удаляет.

    :param file: Загруженный файл
    :return: Извлечённый текст
    """
    temp_file_path = TEMP_DIR / file.filename

    # Сохраняем временный файл
    with temp_file_path.open("wb") as temp_file:
        temp_file.write(await file.read())

    try:
        # Парсим содержимое файла
        start_section = "ФУНКЦИЯ ОТСЛЕЖИВАНИЯ ИЗМЕНЕНИЙ POSTING"
        end_section = "ПРИЛОЖЕНИЯ"
        sections = ["ФУНКЦИЯ ОТСЛЕЖИВАНИЯ ИЗМЕНЕНИЙ POSTING", "P/V модуль XYZAR01R"]
        extracted_text = extract_sections_from_docx(temp_file_path, start_section, end_section, sections)
    finally:
        # Удаляем временный файл
        temp_file_path.unlink()

    return extracted_text
