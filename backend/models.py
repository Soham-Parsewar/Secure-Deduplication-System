from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class FileMetadata(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255))
    file_hash = Column(String(64), unique=True, index=True)
    file_path = Column(String(500))
    merkle_root = Column(String(64))

class PerformanceLog(Base):
    __tablename__ = "performance"
    id = Column(Integer, primary_key=True, index=True)
    algorithm = Column(String(50))
    encryption_time = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
