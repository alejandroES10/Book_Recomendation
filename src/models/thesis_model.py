from sqlalchemy import Column, Integer, String, Boolean, BigInteger, Text, JSON, DateTime
from sqlalchemy.orm import declarative_base
from enum import Enum
from sqlalchemy import Enum as SqlEnum


Base = declarative_base()

class ThesisModel(Base):
    __tablename__ = 'thesis'

    id = Column(Integer, primary_key=True)
    handle = Column(Text, nullable=False, unique=True, index=True)
    metadata_json = Column(JSON, nullable=False)
    original_name_document = Column(Text, nullable=False)
    size_bytes_document = Column(BigInteger, nullable=False)
    download_url = Column(Text, nullable=False)
    is_vectorized = Column(Boolean, default=False, index=True)



class ProcessName(str, Enum):
    IMPORT_THESIS = "import_thesis"
    VECTORIZE_THESIS = "vectorize_thesis"

class ProcessStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class ProcessStatusModel(Base):
    __tablename__ = "process_status"

    id = Column(Integer, primary_key=True)
    process_name = Column(SqlEnum(ProcessName), unique=True, nullable=False, index=True)
    status = Column(SqlEnum(ProcessStatus), nullable=False)
    started_at = Column(DateTime)
    ended_at = Column(DateTime)
    error_messages = Column(JSON)
