from fastapi import APIRouter, File, UploadFile, HTTPException
import crud.generative_model


router = APIRouter()


@router.post("")
async def readable_specification(file: UploadFile):
    if file.filename.endswith(".docx"):
        try:
            result = await crud.generative_model.get_readable_specification(file)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing file: {e}")

    else:
        raise HTTPException(status_code=400, detail="Invalid file format. Only .docx files are supported.")

    return {"extracted_text": result}
