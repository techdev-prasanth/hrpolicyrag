from sqlalchemy import Column,String,Integer , DateTime
from database import Base
from sqlalchemy.sql import func

class PDFFile(Base):
    __tablename__ = "pdffile"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_id = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    