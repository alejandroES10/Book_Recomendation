from abc import ABC, abstractmethod
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_postgres import PostgresChatMessageHistory

from src.database.postgres.chats.custom_postgres_chat_message_history import CustomPostgresChatMessageHistory
# from langchain_community.chat_message_histories import (
#     PostgresChatMessageHistory,
# )


class BaseChatWithDatabase(ABC):
    """Clase base para manejar la conexión a la base de datos y el historial de mensajes."""

    @abstractmethod
    def get_chat_history(self, session_id: str)  -> BaseChatMessageHistory:
        """Método abstracto para obtener la conexión a la base de datos."""
        pass

# class ChatWithPostgres(BaseChatWithDatabase):


#     """Clase para manejar la conexión a la base de datos PostgreSQL y el historial de mensajes."""

#     def get_chat_history(self, session_id: str) -> BaseChatMessageHistory:
#         """Devuelve una instancia de PostgresChatMessageHistory con los datos de conexión."""
#         return PostgresChatMessageHistory(
#             connection_string="postgresql://postgres:postgres@localhost/chat",
#             session_id=session_id,
#         )



import psycopg
from langchain_postgres import PostgresChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory


class ChatWithPostgres(BaseChatWithDatabase):
    def __init__(self):
        self.connection = None
        self.table_name = "chat_history"

    def init_connection(self):
        self.connection = psycopg.connect("postgresql://postgres:postgres@localhost/chats")
        CustomPostgresChatMessageHistory.create_tables(self.connection, self.table_name)

    def get_chat_history(self, session_id: str) -> BaseChatMessageHistory:
        self.init_connection()
       
        
        return CustomPostgresChatMessageHistory(
            self.table_name,
            session_id,
            max_messages=10,
            sync_connection=self.connection)
