from fastapi import APIRouter, File, UploadFile, HTTPException
from crud.file_handler import process_uploaded_file
from docx import Document
from spacy.lang.ru import Russian

router = APIRouter()
doc = Document()


@router.post("/upload_file")
async def upload_file(file: UploadFile):
    # Проверяем формат файла
    if file.filename.endswith(".docx"):
        try:
            result = await process_uploaded_file(file)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing file: {e}")

    else:
        raise HTTPException(status_code=400, detail="Invalid file format. Only .docx files are supported.")

    return {"extracted_text": result}
