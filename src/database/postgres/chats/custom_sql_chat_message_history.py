from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.messages import BaseMessage
from typing import Dict, List, Sequence

from sqlalchemy import select



class CustomSQLChatMessageHistory(SQLChatMessageHistory):
    def __init__(self, *args, max_messages: int = 10, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_messages = max_messages

    def _enforce_limit(self, session):
        messages_query = (
            session.query(self.sql_model_class)
            .filter(getattr(self.sql_model_class, self.session_id_field_name) == self.session_id)
            .order_by(self.sql_model_class.id.asc())
        )
        total = messages_query.count()
        if total > self.max_messages:
            to_delete = total - self.max_messages
            old_messages = messages_query.limit(to_delete).all()
            for msg in old_messages:
                session.delete(msg)

    def add_message(self, message: BaseMessage) -> None:
        with self._make_sync_session() as session:
            session.add(self.converter.to_sql_model(message, self.session_id))
            self._enforce_limit(session)
            session.commit()

    async def aadd_message(self, message: BaseMessage) -> None:
        await self._acreate_table_if_not_exists()
        async with self._make_async_session() as session:
            session.add(self.converter.to_sql_model(message, self.session_id))
            await session.flush()
            await self._aenforce_limit(session)
            await session.commit()

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        with self._make_sync_session() as session:
            for message in messages:
                session.add(self.converter.to_sql_model(message, self.session_id))
            self._enforce_limit(session)
            session.commit()

    async def aadd_messages(self, messages: Sequence[BaseMessage]) -> None:
        await self._acreate_table_if_not_exists()
        async with self._make_async_session() as session:
            for message in messages:
                session.add(self.converter.to_sql_model(message, self.session_id))
            await session.flush()
            await self._aenforce_limit(session)
            await session.commit()

    async def _aenforce_limit(self, session):
        stmt = (
            select(self.sql_model_class)
            .where(getattr(self.sql_model_class, self.session_id_field_name) == self.session_id)
            .order_by(self.sql_model_class.id.asc())
        )
        result = await session.execute(stmt)
        all_messages = result.scalars().all()
        total = len(all_messages)
        if total > self.max_messages:
            to_delete = all_messages[: total - self.max_messages]
            for msg in to_delete:
                await session.delete(msg)

    # async def aget_raw_messages(self) -> List:
    #         """Devuelve los mensajes tal como están en la tabla SQL (sin convertir a BaseMessage)"""
    #         await self._acreate_table_if_not_exists()
    #         async with self._make_async_session() as session:
    #             stmt = (
    #                 select(self.sql_model_class)
    #                 .where(
    #                     getattr(self.sql_model_class, self.session_id_field_name)
    #                     == self.session_id
    #                 )
    #                 .order_by(self.sql_model_class.id.asc())
    #             )
    #             result = await session.execute(stmt)
    #             return result.scalars().all()  # <- Aquí no se aplica self.converter

    async def aget_raw_messages(self) -> List[Dict]:
        """Devuelve los mensajes sin la columna 'id' (versión síncrona)"""
        await self._acreate_table_if_not_exists()
        async with self._make_async_session() as session:
            # Seleccionar campos específicos (excluyendo 'id')
            stmt = (
                select(
                    self.sql_model_class.session_id,
                    self.sql_model_class.type,
                    self.sql_model_class.content,
                    self.sql_model_class.created_at
                )
                .where(
                    getattr(self.sql_model_class, self.session_id_field_name) == self.session_id
                )
                .order_by(self.sql_model_class.id.asc())
            )
            result = await session.execute(stmt)
            rows = result.all()
            # Convertimos cada fila a dict
            return [
                {
                    "session_id": r[0],
                    "type": r[1],
                    "content": r[2],
                    "created_at": r[3]
                }
                for r in rows
            ]
        
    def get_raw_messages(self) -> List[Dict]:
        """Devuelve los mensajes sin la columna 'id' (versión síncrona)"""
        self._create_table_if_not_exists()
        with self._make_sync_session() as session:
            # Seleccionar campos específicos (excluyendo 'id')
            stmt = (
                select(
                    self.sql_model_class.session_id,
                    self.sql_model_class.type,
                    self.sql_model_class.content,
                    self.sql_model_class.created_at
                )
                .where(
                    getattr(self.sql_model_class, self.session_id_field_name) == self.session_id
                )
                .order_by(self.sql_model_class.id.asc())
            )
            result = session.execute(stmt)
            rows = result.fetchall()
            return [
                {
                    "session_id": r[0],
                    "type": r[1],
                    "content": r[2],
                    "created_at": r[3]
                }
                for r in rows
            ]
