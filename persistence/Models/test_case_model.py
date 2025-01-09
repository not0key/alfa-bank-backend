from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TestCase(Base):
    __tablename__ = 'test_cases'

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, index=True)
    processed_result = Column(Text)
    status = Column(String)
