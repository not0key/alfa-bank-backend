from fastapi import FastAPI
from api import generative_model, file_parser, readable_specification, test_cases, users, upload_files
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем запросы с любого источника
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы (GET, POST, PUT и т.д.)
    allow_headers=["*"],  # Разрешаем все заголовки
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(file_parser.router, prefix="/fileParsing", tags=["File Parsing"])
app.include_router(generative_model.router, prefix="/generativeModel", tags=["GenerativeModel"])
app.include_router(readable_specification.router, prefix="/readableSpecification", tags=["ReadableSpecification"])
app.include_router(test_cases.router, prefix="/testCases", tags=["TestCases"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(upload_files.router, prefix="/uploadFiles", tags=["Upload Files"])
