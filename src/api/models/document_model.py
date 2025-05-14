
from pydantic import BaseModel

class BookMetadataModel(BaseModel):
    id: str 
    # page_content: str
    metadata: dict
  