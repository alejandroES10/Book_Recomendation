from pydantic import BaseModel
from typing import List, Optional
from src.api.schemas.message_schema import MessageSchema



class ChatHistoryModel(BaseModel):
    session_id: str
    history: List[MessageSchema]
