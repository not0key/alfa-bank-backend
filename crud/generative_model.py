from crud.file_handler import process_uploaded_file
from utils.generative_model_utlis import send_message
from dotenv import load_dotenv
import os
from pydantic import BaseModel

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


async def create_test_cases(file):
    parsed_text = await process_uploaded_file(file)
    result = []

    for section in parsed_text.keys():
        parsed_text[section] = "\n".join(parsed_text[section])

        result.append(await send_message(os.getenv("prompt_readable_specification") + parsed_text[section]))

    return result