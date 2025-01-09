from sqlalchemy.orm import Session
from persistence.Models.test_case_model import TestCase  # Импортируйте вашу модель



def save_test_case(db: Session, file_name: str, result: str, status:str):
    file_entry = TestCase(file_name=file_name, processed_result=result, status=status)
    db.add(file_entry)
    db.commit()
    db.refresh(file_entry)
    return file_entry