from fastapi import FastAPI
from api import generative_model, file_parser


app = FastAPI()

app.include_router(file_parser.router, prefix="/file_parsing", tags=["File Parsing"])


app.include_router(generative_model.router, prefix="/ChatGpt", tags=["ChatGpt"])

# Простой тестовый эндпоинт для проверки работы сервера
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
app.include_router(generative_model.router, prefix="/GenerativeModel", tags=["GenerativeModel"])
