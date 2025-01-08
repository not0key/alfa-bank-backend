from fastapi import FastAPI
from api import generative_model, file_parser, readable_specification, test_cases, users


app = FastAPI()

app.include_router(file_parser.router, prefix="/fileParsing", tags=["File Parsing"])


app.include_router(generative_model.router, prefix="/chatGpt", tags=["ChatGpt"])

app.include_router(generative_model.router, prefix="/generativeModel", tags=["GenerativeModel"])

app.include_router(readable_specification.router, prefix="/readableSpecification", tags=["ReadableSpecification"])

app.include_router(test_cases.router, prefix="/testCases", tags=["TestCases"])

app.include_router(users.router, prefix="/users", tags=["Users"])
