from fastapi import APIRouter, File, UploadFile, HTTPException
from crud.file_handler import process_uploaded_file
from docx import Document

router = APIRouter()
doc = Document()
@router.post("/")
async def upload_file(file: UploadFile):
    # Проверяем формат файла
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Invalid file format. Only .docx files are supported.")

    # Обрабатываем файл
    try:
        result = await process_uploaded_file(file)
        for string in result:
            doc.add_paragraph(string)

        doc.save("test_output.docx")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {e}")

    return {"extracted_text": result}
