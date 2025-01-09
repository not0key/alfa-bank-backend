from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from persistence.database import SessionLocal
from utils.upload_files_utils import save_file, save_file_to_db, get_files_from_db, get_file_response

router = APIRouter()


def get_db():
    """Получает сессию базы данных."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload/")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Маршрут для загрузки файла."""
    try:
        # Сохраняем файл на сервере
        new_file = save_file(file, db)

        # Сохраняем информацию о файле в базе данных
        #new_file = save_file_to_db(db, file, file_location)

        return {"id": new_file.id, "filename": new_file.filename, "filepath": new_file.filepath}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/files")
def list_files(db: Session = Depends(get_db)):
    """Маршрут для получения списка файлов."""
    return get_files_from_db(db)


@router.get("/{filename}")
async def get_static_file(filename: str):
    """Маршрут для получения файла."""
    try:
        return get_file_response(filename)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
