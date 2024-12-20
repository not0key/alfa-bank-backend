from fastapi import APIRouter, File, UploadFile, HTTPException
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


client = OpenAI(
    api_key=os.getenv("api_key")
)


class ChatRequest(BaseModel):
    prompt: str


async def send_message(prompt):
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        print(completion)
        print(completion.choices[0].message)

        return {"response": completion.choices[0].message}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))