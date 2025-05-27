from abc import ABC, abstractmethod
from typing import List

from src.schemas.chat_history_schema import ChatHistorySchema


class IChatService(ABC):

    @abstractmethod
    async def get_chat_bot_answer(self,session_id: str, input: str) -> str:
        pass

    @abstractmethod
    async def get_chat_history(self,session_id: str) -> ChatHistorySchema:
        pass

    @abstractmethod   
    async def delete_chat_history(self,session_id: str) -> None:
        pass

    