from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from persistence.database import Base


class UploadFile(Base):
    __tablename__ = "upload_files"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    filepath = Column(String)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
