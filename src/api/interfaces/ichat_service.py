from abc import ABC
from typing import List

from src.api.models.chat_history_model import ChatHistoryModel


class IChatService(ABC):

    def __init__(self):
        pass
  
    async def get_chat_bot_answer(session_id: str, input: str) -> str:
        pass

    async def get_chat_history(session_id: str) -> ChatHistoryModel:
        pass

    async def delete_chat_history(session_id: str) -> None:
        pass

    