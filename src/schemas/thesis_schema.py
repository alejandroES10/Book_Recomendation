from pydantic import BaseModel
from typing import Dict

class ThesisSchema(BaseModel):
    handle: str
    metadata_json: Dict
    original_name: str
    size_bytes: int
    download_url: str
    checksum_md5: str
    is_processed: bool = False
