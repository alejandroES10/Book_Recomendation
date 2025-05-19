from pydantic import BaseModel
from typing import Optional

class MessageModel(BaseModel):
    type: str
    content: str
    created_at: Optional[str]