from fastapi import FastAPI, HTTPException

from api.endpoints import file_parser, generative_model
from pydantic import BaseModel
from openai import OpenAI
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


app.include_router(file_parser.router, prefix="/api/v1", tags=["File Parsing"])

class ChatRequest(BaseModel):
    message: str

# Функция для генерации ответа с использованием ChatGPT
def generate_response(prompt: str) -> str:
    client = OpenAI(
        api_key="api-key",  # This is the default and can be omitted
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Say this is a test",
            }
        ],
        model="gpt-4o-mini",
    )

@app.post("/chat/")
async def chat_with_gpt(request: ChatRequest):
    # Получаем сообщение от пользователя
    user_message = request.message
    # Генерируем ответ с использованием ChatGPT
    response = generate_response(user_message)
    # Возвращаем ответ
    return {"reply": response}

# Простой тестовый эндпоинт для проверки работы сервера
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}