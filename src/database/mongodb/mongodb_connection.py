from abc import ABC, abstractmethod
import os
from dotenv import load_dotenv
from src.database.mongodb.limited_mongodb_chat_message_history import LimitedMongoDBChatMessageHistory



class MongoDBConnection:
    @staticmethod
    def get_connection(session_id: str) -> LimitedMongoDBChatMessageHistory:
        """Devuelve una instancia de LimitedMongoDBChatMessageHistory con los datos de conexión."""
        return LimitedMongoDBChatMessageHistory(
            session_id=session_id,
            connection_string=os.getenv("MONGO_CONNECTION_STRING"),
            database_name=os.getenv("MONGO_DATABASE_NAME"),
            collection_name=os.getenv("MONGO_COLLECTION_NAME"),
            create_index=True,
            max_history=10  # Configura el historial limitado
        )


# import os
# from pymongo import MongoClient
# from dotenv import load_dotenv

# load_dotenv()

# class MongoDBClientSingleton:
#     _client = None

#     @classmethod
#     def get_client(cls) -> MongoClient:
#         if cls._client is None:
#             connection_string = os.getenv("MONGO_CONNECTION_STRING")
#             cls._client = MongoClient(connection_string)
#         return cls._client




# class MongoDBConnection:
#     @staticmethod
#     def get_history(session_id: str) -> LimitedMongoDBChatMessageHistory:
#         # client = MongoDBClientSingleton.get_client()
#         # db = client[os.getenv("MONGO_DATABASE_NAME")]
#         return LimitedMongoDBChatMessageHistory(
#             session_id=session_id,
#             connection_string=MongoDBClientSingleton.get_client(),
#             database_name=os.getenv("MONGO_DATABASE_NAME"),
#             collection_name=os.getenv("MONGO_COLLECTION_NAME"),
#             create_index=True,
#             max_history=10
#         )
