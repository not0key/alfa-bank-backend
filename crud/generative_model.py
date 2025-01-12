from crud.file_handler import process_uploaded_file, process_file
from utils.generative_model_utlis import send_message
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from utils import test_cases_utils
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from persistence.database import engine
from utils.upload_files_utils import save_file, save_file_to_db
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from pathlib import Path

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

load_dotenv()


class ChatRequest(BaseModel):
    prompt: str


async def get_readable_specification(file):
    parsed_text = await process_uploaded_file(file)
    readable_specification = []

    for section in parsed_text.keys():
        parsed_text[section] = "\n".join(parsed_text[section])
        readable_specification.append(await send_message(os.getenv("prompt_readable_specification") + '\n' + parsed_text[section]))

    result = '<br/>'.join(readable_specification).replace('\n', '<br/>')
    return result


async def create_test_cases(file: UploadFile, db: Session):
    try:
        # Сохраняем файл на сервере
        new_file = save_file(file, db)
        file_path = Path(new_file.filepath)  # Используем путь из базы данных
    except Exception as e:
        print(f"Error during file save: {e}")
        raise

    # Обработка загруженного файла через путь
    parsed_text = await process_file(file_path)
    if len(parsed_text) == 0:
        return f"Неверная структура файла"
    test_cases = []

    for section in parsed_text.keys():
        parsed_text[section] = "\n".join(parsed_text[section])
        #test_cases.append(parsed_text[section])
        test_case = (await send_message(os.getenv("prompt_test_cases") + '\n' + parsed_text[section]))
        test_cases.append(test_case)

    result = '<br/>'.join(test_cases).replace('\n', '<br/>')
    test_cases_utils.save_test_case(db, new_file.filename, result, status="Выполнена")
    return result
