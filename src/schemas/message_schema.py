from pydantic import BaseModel
from typing import Optional

class MessageSchema(BaseModel):
    type: str
    content: str
    created_at: Optional[str]