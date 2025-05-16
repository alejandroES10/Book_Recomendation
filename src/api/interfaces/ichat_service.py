from abc import ABC, abstractmethod
from typing import List

from src.api.models.chat_history_model import ChatHistoryModel


class IChatService(ABC):

    @abstractmethod
    async def get_chat_bot_answer(session_id: str, input: str) -> str:
        pass

    @abstractmethod
    async def get_chat_history(session_id: str) -> ChatHistoryModel:
        pass

    @abstractmethod   
    async def delete_chat_history(session_id: str) -> None:
        pass

    