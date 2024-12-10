from fastapi import APIRouter, File, UploadFile, HTTPException
from openai import OpenAI
from pydantic import BaseModel


class ChatRequest(BaseModel):
    prompt: str
    max_tokens: int = 50


router = APIRouter()


@router.post("/chat")
async def send_message(request: ChatRequest):
    try:
        print(request)
        client = OpenAI(
            api_key="api-key",
        )
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": request.prompt}
            ]
        )

        print(completion)
        print(completion.choices[0].message)

        return {"response": completion.choices[0].message}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
