from fastapi import APIRouter
from pydantic import BaseModel
from utils import generative_model_utlis


router = APIRouter()


class ChatRequest(BaseModel):
    prompt: str


@router.post("/chat", response_model=None)
async def send_message(request: ChatRequest):
    print(1)
    return await generative_model_utlis.send_message(request.prompt)
