
from pydantic import BaseModel

class ChatModel(BaseModel):
    session_id: str 
    page_content: str
    metadata: dict
  