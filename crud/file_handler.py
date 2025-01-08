from pathlib import Path
from utils.file_utils import extract_sections_from_docx

TEMP_DIR = Path("temp")  # Директория для временных файлов
TEMP_DIR.mkdir(exist_ok=True)  # Убедимся, что папка существует


async def process_uploaded_file(file):
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
        sections = [("Опция XYZ", "P/V модуль"), ("P/V модуль", "Приложения")]
        extracted_text = extract_sections_from_docx(temp_file_path, sections)
    finally:
        # Удаляем временный файл
        temp_file_path.unlink()

    return extracted_text
