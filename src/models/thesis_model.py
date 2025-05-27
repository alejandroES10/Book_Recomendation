from sqlalchemy import Column, Integer, String, Boolean, BigInteger, Text, JSON
from sqlalchemy.orm import declarative_base
Base = declarative_base()

class Thesis(Base):
    __tablename__ = 'thesis'

    id = Column(Integer, primary_key=True)
    handle = Column(String(255), nullable=False, unique=True, index=True)
    metadata_json = Column(JSON, nullable=False)
    original_name = Column(String(255), nullable=False)
    size_bytes = Column(BigInteger, nullable=False)
    download_url = Column(Text, nullable=False)
    checksum_md5 = Column(String(32), nullable=False)
    is_processed = Column(Boolean, default=False, index=True)
