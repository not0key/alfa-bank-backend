from fastapi import APIRouter, File, UploadFile, HTTPException,Depends
import crud.generative_model
from sqlalchemy.orm import Session
from persistence.Models import test_case_model
from persistence.database import SessionLocal, engine

test_case_model.Base.metadata.create_all(bind=engine)

router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("")
async def create_test_cases(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.filename.endswith(".docx"):
        try:
            result = await crud.generative_model.create_test_cases(file, db)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing file: {e}")

    else:
        raise HTTPException(status_code=400, detail="Invalid file format. Only .docx files are supported.")

    return {"test_cases": result}
