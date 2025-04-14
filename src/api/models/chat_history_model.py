from pydantic import BaseModel
from typing import List, Optional
from src.api.models.message_model import MessageModel



class ChatHistoryModel(BaseModel):
    session_id: str
    history: List[MessageModel]
