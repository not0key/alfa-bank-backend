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


@router.get("")
async def get_test_cases(db: Session = Depends(get_db)):
    return db.query(test_case_model.TestCase).all()


@router.get("/{test_case_id}")
async def get_test_case(test_case_id: int, db: Session = Depends(get_db)):
    # Попытаться получить тест по ID
    test_case = db.query(test_case_model.TestCase).filter(test_case_model.TestCase.id == test_case_id).first()

    if test_case is None:
        raise HTTPException(status_code=404, detail="Test case not found")

    return test_case