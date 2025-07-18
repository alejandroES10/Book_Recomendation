from pydantic import BaseModel
from typing import List, Optional
from src.schemas.message_schema import MessageSchema



class ChatHistorySchema(BaseModel):
    session_id: str
    history: List[MessageSchema]
