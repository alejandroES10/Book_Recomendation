from datetime import datetime
from typing import Any

import sqlalchemy as sa
from sqlalchemy.orm import declarative_base
from langchain_community.chat_message_histories.sql import BaseMessageConverter
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage

from src.database.postgres.chats.custom_sql_chat_message_history import CustomSQLChatMessageHistory


# Declarar base para el modelo
Base = declarative_base()

# Modelo de mensaje
class CustomMessage(Base):
    __tablename__ = "custom_message_store"

    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    session_id = sa.Column(sa.Text, index=True)  
    type = sa.Column(sa.Text)
    content = sa.Column(sa.Text)
    created_at = sa.Column(sa.DateTime)

# Convertidor personalizado
class CustomMessageConverter(BaseMessageConverter):
    def __init__(self):
        super().__init__()

    def from_sql_model(self, sql_message: Any) -> BaseMessage:
        if sql_message.type == "human":
            return HumanMessage(content=sql_message.content)
        elif sql_message.type == "ai":
            return AIMessage(content=sql_message.content)
        elif sql_message.type == "system":
            return SystemMessage(content=sql_message.content)
        else:
            raise ValueError(f"Unknown message type: {sql_message.type}")

    def to_sql_model(self, message: BaseMessage, session_id: str) -> Any:
        return CustomMessage(
            session_id=session_id,
            type=message.type,
            content=message.content,
            created_at=datetime.now()
        )

    def get_sql_model_class(self) -> Any:
        return CustomMessage
    

from abc import ABC, abstractmethod
from langchain_core.chat_history import BaseChatMessageHistory
# from langchain_postgres import PostgresChatMessageHistory
from src.database.postgres.chats.postg import PostgresChatMessageHistory
from psycopg_pool import AsyncConnectionPool

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


# class ChatWithPostgres(BaseChatWithDatabase):
#     def __init__(self):
#         self.connection = None
#         self.table_name = "chat_history"

#     def init_connection(self):
#         self.connection = psycopg.connect("postgresql://postgres:postgres@localhost/chats")
#         CustomPostgresChatMessageHistory.create_tables(self.connection, self.table_name)

#     def get_chat_history(self, session_id: str) -> BaseChatMessageHistory:
#         self.init_connection()
       
#         return CustomPostgresChatMessageHistory(
#             self.table_name,
#             session_id,
#             max_messages=10,
#             sync_connection=self.connection)


# class ChatWithPostgres(BaseChatWithDatabase):
#     def __init__(self):
#         self.pool = AsyncConnectionPool(conninfo="postgresql://postgres:postgres@localhost/chats")
#         self.table_name = "chat_history"

#     # async def init_connection(self):
#     #     # self.connection = await psycopg.AsyncConnection.connect("postgresql://postgres:postgres@localhost/chats")
#     #     # await CustomPostgresChatMessageHistory.acreate_tables(self.connection, self.table_name)

#     #     self.pool = AsyncConnectionPool(conninfo="postgresql://postgres:postgres@localhost/chats")

#     def get_chat_history(self, session_id: str) -> BaseChatMessageHistory:
       
#         return PostgresChatMessageHistory(
#             session_id=session_id,
#             table_name=self.table_name,
#             conn_pool=self.pool,
#         )


# from psycopg_pool import AsyncConnectionPool
# from langchain_postgres import PostgresChatMessageHistory
# from langchain_core.chat_history import BaseChatMessageHistory

# class ChatWithPostgres(BaseChatWithDatabase):
#     def __init__(self):
#         self._pool = None  # Inicializamos como None
#         self.table_name = "chat_history"
    
#     async def get_pool(self):
#         """Obtiene el pool de conexiones, inicializándolo si es necesario"""
#         if self._pool is None:
#             self._pool = AsyncConnectionPool(
#                 conninfo="postgresql://postgres:postgres@localhost/chats",
#                 open=False  # No abrir inmediatamente
#             )
#             await self._pool.open()  # Abrimos explícitamente cuando tenemos un event loop
#         return self._pool

#     async def get_chat_history(self, session_id: str) -> BaseChatMessageHistory:
#         pool = await self.get_pool()
#         return PostgresChatMessageHistory(
#             session_id=session_id,
#             table_name=self.table_name,
#             conn_pool=pool,
#         )

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/chats"
from sqlalchemy.ext.asyncio import create_async_engine
from langchain_community.chat_message_histories import SQLChatMessageHistory

class ChatWithPostgres(BaseChatWithDatabase):
    def __init__(self):
        self._connection = self.init_connection()
        

    def init_connection(self):
        """Inicializa la conexión a la base de datos PostgreSQL."""
        return create_async_engine(url=
            DATABASE_URL)
        
        

    def get_chat_history(self, session_id: str) -> BaseChatMessageHistory:
        return CustomSQLChatMessageHistory(
            session_id=session_id,
            connection=self._connection,
            engine_args={"echo": False},
			custom_message_converter=CustomMessageConverter()
        )
