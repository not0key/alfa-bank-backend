from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import APIRouter, File, UploadFile, HTTPException
from openai import OpenAI
from pydantic import BaseModel
import crud.generative_model
from dotenv import load_dotenv
import os
from utils import generative_model_utlis


router = APIRouter()


class ChatRequest(BaseModel):
    prompt: str


@router.post("/chat", response_model=None)
async def send_message(request: ChatRequest):
    print(1)
    return await generative_model_utlis.send_message(request.prompt)


@router.post("/readable_specification")
async def readable_specification(file: UploadFile):
    if file.filename.endswith(".docx"):
        try:
            result = await crud.generative_model.get_readable_specification(file)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing file: {e}")

    else:
        raise HTTPException(status_code=400, detail="Invalid file format. Only .docx files are supported.")

    return {"extracted_text": result}


@router.post("/create_test_cases")
async def create_test_cases(file: UploadFile):
    if file.filename.endswith(".docx"):
        try:
            result = await crud.generative_model.create_test_cases(file)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing file: {e}")

    else:
        raise HTTPException(status_code=400, detail="Invalid file format. Only .docx files are supported.")

    return {"extracted_text": result}
