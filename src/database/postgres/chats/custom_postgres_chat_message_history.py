import re
import json
from typing import Optional, Sequence
from langchain_postgres import PostgresChatMessageHistory
import psycopg
from psycopg import logger, sql
from langchain_core.messages import BaseMessage
from typing import List
from psycopg import sql

def _create_custom_table_and_index(table_name: str) -> List[sql.Composed]:
        """Create SQL statements for table with session_id as TEXT."""
        index_name = f"idx_{table_name}_session_id"
        statements = [
            sql.SQL(
                """
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id SERIAL PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    message JSONB NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                );
                """
            ).format(table_name=sql.Identifier(table_name)),
            sql.SQL(
                """
                CREATE INDEX IF NOT EXISTS {index_name} ON {table_name} (session_id);
                """
            ).format(
                table_name=sql.Identifier(table_name),
                index_name=sql.Identifier(index_name)
            ),
        ]
        return statements

class CustomPostgresChatMessageHistory(PostgresChatMessageHistory):
    def __init__(
        self,
        table_name: str,
        session_id: str,
        /,
        *,
        max_messages: Optional[int] = None,
        sync_connection: Optional[psycopg.Connection] = None,
        async_connection: Optional[psycopg.AsyncConnection] = None,
    ) -> None:
        if not sync_connection and not async_connection:
            raise ValueError("Must provide sync_connection or async_connection")

        self._connection = sync_connection
        self._aconnection = async_connection
        self._session_id = session_id
        self._max_messages = max_messages

        if not re.match(r"^\w+$", table_name):
            raise ValueError(
                "Invalid table name. Table name must contain only alphanumeric characters and underscores."
            )
        self._table_name = table_name



    # @staticmethod
    # def create_tables(connection: psycopg.Connection, table_name: str) -> None:
    #     queries = _create_custom_table_and_index(table_name)
    #     with connection.cursor() as cursor:
    #         for query in queries:
    #             cursor.execute(query)
    #     connection.commit()

    # @staticmethod
    # async def acreate_tables(connection: psycopg.AsyncConnection, table_name: str) -> None:
    #     queries = _create_custom_table_and_index(table_name)
    #     async with connection.cursor() as cursor:
    #         for query in queries:
    #             await cursor.execute(query)
    #     await connection.commit()

    @staticmethod
    def create_tables(
        connection: psycopg.Connection,
        table_name: str,
        /,
    ) -> None:
        """Create the table schema in the database and create relevant indexes."""
        queries = _create_custom_table_and_index(table_name)
        logger.info("Creating schema for table %s", table_name)
        with connection.cursor() as cursor:
            for query in queries:
                cursor.execute(query)
        connection.commit()

    @staticmethod
    async def acreate_tables(
        connection: psycopg.AsyncConnection, table_name: str, /
    ) -> None:
        """Create the table schema in the database and create relevant indexes."""
        queries = _create_custom_table_and_index(table_name)
        logger.info("Creating schema for table %s", table_name)
        async with connection.cursor() as cur:
            for query in queries:
                await cur.execute(query)
        await connection.commit()






    # @staticmethod
    # def create_tables(connection: psycopg.Connection, table_name: str) -> None:
    #     query = f"""
    #         CREATE TABLE IF NOT EXISTS {table_name} (
    #             id SERIAL PRIMARY KEY,
    #             session_id TEXT NOT NULL,
    #             message JSONB NOT NULL,
    #             created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    #         );
    #         CREATE INDEX IF NOT EXISTS idx_{table_name}_session_id ON {table_name} (session_id);
    #     """
    #     with connection.cursor() as cursor:
    #         cursor.execute(query)
    #     connection.commit()

    # @staticmethod
    # async def acreate_tables(connection: psycopg.AsyncConnection, table_name: str) -> None:
    #     query = f"""
    #         CREATE TABLE IF NOT EXISTS {table_name} (
    #             id SERIAL PRIMARY KEY,
    #             session_id TEXT NOT NULL,
    #             message JSONB NOT NULL,
    #             created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    #         );
    #         CREATE INDEX IF NOT EXISTS idx_{table_name}_session_id ON {table_name} (session_id);
    #     """
    #     async with connection.cursor() as cursor:
    #         await cursor.execute(query)
    #     await connection.commit()

    def _ensure_max_messages_sync(self):
        if self._max_messages is None or self._connection is None:
            return

        query_count = sql.SQL(
            f"SELECT COUNT(*) FROM {self._table_name} WHERE session_id = %s"
        )
        query_delete = sql.SQL(
            f"""
            DELETE FROM {self._table_name}
            WHERE id IN (
                SELECT id FROM {self._table_name}
                WHERE session_id = %s
                ORDER BY created_at ASC
                LIMIT %s
            );
            """
        )
        with self._connection.cursor() as cur:
            cur.execute(query_count, (self._session_id,))
            total = cur.fetchone()[0]
            if total > self._max_messages:
                to_delete = total - self._max_messages
                cur.execute(query_delete, (self._session_id, to_delete))
        self._connection.commit()

    async def _ensure_max_messages_async(self):
        if self._max_messages is None or self._aconnection is None:
            return

        query_count = sql.SQL(
            f"SELECT COUNT(*) FROM {self._table_name} WHERE session_id = %s"
        )
        query_delete = sql.SQL(
            f"""
            DELETE FROM {self._table_name}
            WHERE id IN (
                SELECT id FROM {self._table_name}
                WHERE session_id = %s
                ORDER BY created_at ASC
                LIMIT %s
            );
            """
        )
        async with self._aconnection.cursor() as cur:
            await cur.execute(query_count, (self._session_id,))
            total = (await cur.fetchone())[0]
            if total > self._max_messages:
                to_delete = total - self._max_messages
                await cur.execute(query_delete, (self._session_id, to_delete))
        await self._aconnection.commit()

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        super().add_messages(messages)
        self._ensure_max_messages_sync()

    async def aadd_messages(self, messages: Sequence[BaseMessage]) -> None:
        await super().aadd_messages(messages)
        await self._ensure_max_messages_async()

    def get_all_messages_for_session(self) -> List[dict]:
        """Fetch all messages and metadata for the current session_id."""
        if self._connection is None:
            raise ValueError("No sync_connection provided.")

        query = sql.SQL(
            "SELECT id, session_id, message, created_at "
            "FROM {table_name} "
            "WHERE session_id = %s "
            "ORDER BY id;"
        ).format(table_name=sql.Identifier(self._table_name))

        with self._connection.cursor() as cur:
            cur.execute(query, (self._session_id,))
            rows = cur.fetchall()

        result = []
        for row in rows:
            result.append({
                "id": row[0],
                "session_id": row[1],
                "message": row[2],
                "created_at": row[3],
            })
        return result

    async def aget_all_messages_for_session(self) -> List[dict]:
        """Asynchronously fetch all messages and metadata for the current session_id."""
        if self._aconnection is None:
            raise ValueError("No async_connection provided.")

        query = sql.SQL(
            "SELECT id, session_id, message, created_at "
            "FROM {table_name} "
            "WHERE session_id = %s "
            "ORDER BY id;"
        ).format(table_name=sql.Identifier(self._table_name))

        async with self._aconnection.cursor() as cur:
            await cur.execute(query, (self._session_id,))
            rows = await cur.fetchall()

        result = []
        for row in rows:
            result.append({
                "id": row[0],
                "session_id": row[1],
                "message": row[2],
                "created_at": row[3],
            })
        return result
