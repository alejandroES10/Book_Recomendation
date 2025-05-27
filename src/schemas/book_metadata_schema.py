
from pydantic import BaseModel

class BookMetadataSchema(BaseModel):
    id: str 
    # page_content: str
    metadata: dict
  