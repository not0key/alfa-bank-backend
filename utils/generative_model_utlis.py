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
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        print(completion)
        message_content = completion['choices'][0]['message']['content']
        print(message_content)
        return message_content
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))