from fastapi import FastAPI
from api import generative_model, file_parser, readable_specification, test_cases


app = FastAPI()

app.include_router(file_parser.router, prefix="/file_parsing", tags=["File Parsing"])


app.include_router(generative_model.router, prefix="/ChatGpt", tags=["ChatGpt"])

# Простой тестовый эндпоинт для проверки работы сервера
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
app.include_router(generative_model.router, prefix="/generativeModel", tags=["GenerativeModel"])

app.include_router(readable_specification.router, prefix="/readableSpecification", tags=["ReadableSpecification"])

app.include_router(test_cases.router, prefix="/testCases", tags=["TestCases"])
