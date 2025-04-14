from pydantic import BaseModel
from typing import Optional

class MessageModel(BaseModel):
    type: str
    content: str
    timestamp: Optional[str]