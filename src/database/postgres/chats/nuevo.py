from langchain_core.messages import HumanMessage

from langchain_community.chat_message_histories import SQLChatMessageHistory

# create sync sql message history by connection_string
message_history = SQLChatMessageHistory(
    session_id='foo', connection_string='sqlite///:memory.db'
)
message_history.add_message(HumanMessage("hello"))
message_history.message

# create async sql message history using aiosqlite
# from sqlalchemy.ext.asyncio import create_async_engine
#
# async_engine = create_async_engine("sqlite+aiosqlite:///memory.db")
# async_message_history = SQLChatMessageHistory(
#     session_id='foo', connection=async_engine,
# )
# await async_message_history.aadd_message(HumanMessage("hello"))
# await async_message_history.aget_messages()


#*****************
# from sqlalchemy.ext.asyncio import create_async_engine
# from langchain_sql_database.chat_message_histories import SQLChatMessageHistory
# from langchain_core.messages import HumanMessage

# # 1. Cambia la URL de conexión al formato PostgreSQL async
# DATABASE_URL = "postgresql+asyncpg://usuario:contraseña@localhost:5432/tu_basededatos"

# # 2. Crea el motor async con PostgreSQL
# async_engine = create_async_engine(DATABASE_URL, echo=True)

# # 3. Crea el historial de mensajes
# async_message_history = SQLChatMessageHistory(
#     session_id="foo",
#     connection=async_engine,
# )

# # 4. Usa los métodos async
# await async_message_history.aadd_message(HumanMessage(content="Hola desde Postgres!"))
# messages = await async_message_history.aget_messages()

# # 5. Muestra los mensajes
# for msg in messages:
#     print(msg)
