from abc import ABC, abstractmethod
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import (
    PostgresChatMessageHistory,
)


class BaseChatWithDatabase(ABC):
    """Clase base para manejar la conexión a la base de datos y el historial de mensajes."""

    @abstractmethod
    def get_chat_history(self, session_id: str)  -> BaseChatMessageHistory:
        """Método abstracto para obtener la conexión a la base de datos."""
        pass

class ChatWithPostgres(BaseChatWithDatabase):


    """Clase para manejar la conexión a la base de datos PostgreSQL y el historial de mensajes."""

    def get_chat_history(self, session_id: str) -> BaseChatMessageHistory:
        """Devuelve una instancia de PostgresChatMessageHistory con los datos de conexión."""
        return PostgresChatMessageHistory(
            connection_string="postgresql://postgres:postgres@localhost/chat_history",
            session_id=session_id,
        )



