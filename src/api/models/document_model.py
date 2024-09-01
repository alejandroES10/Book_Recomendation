
from pydantic import BaseModel

class DocumentModel(BaseModel):
    id: str 
    page_content: str
    metadata: dict
  