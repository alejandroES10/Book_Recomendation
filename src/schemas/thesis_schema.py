from pydantic import BaseModel
from typing import Dict

class ThesisSchema(BaseModel):
    handle: str
    metadata_json: Dict
    original_name_document: str
    size_bytes_document: int
    download_url: str
    is_vectorized: bool = False
