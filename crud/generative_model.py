from crud.file_handler import process_uploaded_file
from utils.generative_model_utlis import send_message
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from utils import test_cases_utils
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from persistence.database import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

load_dotenv()


class ChatRequest(BaseModel):
    prompt: str


async def get_readable_specification(file):
    parsed_text = await process_uploaded_file(file)
    result = []

    for section in parsed_text.keys():
        parsed_text[section] = "\n".join(parsed_text[section])
        result.append(await send_message(os.getenv("prompt_readable_specification") + parsed_text[section]))

    return result


async def create_test_cases(file, db: Session):
    parsed_text = await process_uploaded_file(file)
    result = []

    for section in parsed_text.keys():
        parsed_text[section] = "\n".join(parsed_text[section])
        result.append(section)
        #result.append(await send_message(os.getenv("prompt_test_cases") + '\n' + parsed_text[section]))

    test_cases_utils.save_test_case(db, file.filename, '\n'.join(result), status="Выполнена")
    return result
