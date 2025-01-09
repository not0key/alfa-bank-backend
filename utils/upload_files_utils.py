from pathlib import Path
from fastapi import UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from persistence.Models.upload_file_model import UploadFile as FileModel
import uuid
import os

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_file(file: UploadFile, db: Session):
    """
    Сохраняет файл на сервере с уникальным именем.
    Возвращает путь к сохранённому файлу.
    """
    # Создаем уникальное имя файла, добавляя UUID
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_location = UPLOAD_DIR / unique_filename

    # Сохраняем файл на диск
    with open(file_location, "wb") as f:
        f.write(file.file.read())
    new_file = FileModel(filename=unique_filename, filepath=str(file_location))

    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return new_file


def save_file_to_db(db: Session, file: UploadFile, file_location: Path) -> FileModel:
    """Сохраняет информацию о файле в базе данных."""
    new_file = FileModel(filename=file.filename, filepath=str(file_location))
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return new_file


def get_files_from_db(db: Session) -> list:
    """Возвращает список всех файлов из базы данных."""
    return db.query(FileModel).all()


def get_file_response(filename: str) -> FileResponse:
    """Возвращает файл в ответе, если он существует."""
    file_path = UPLOAD_DIR / filename
    if file_path.exists():
        return FileResponse(file_path)
    else:
        raise FileNotFoundError(f"File {filename} not found")
