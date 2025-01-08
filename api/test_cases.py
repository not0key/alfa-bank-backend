from fastapi import APIRouter, File, UploadFile, HTTPException
import crud.generative_model


router = APIRouter()


@router.post("")
async def create_test_cases(file: UploadFile):
    if file.filename.endswith(".docx"):
        try:
            result = await crud.generative_model.create_test_cases(file)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing file: {e}")

    else:
        raise HTTPException(status_code=400, detail="Invalid file format. Only .docx files are supported.")

    return {"test_cases": result}
