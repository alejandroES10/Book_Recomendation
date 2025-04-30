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


# class MongoDBConnection:
#     _instance = None

#     def __new__(cls, session_id: str = None):
#         # Se crea una instancia solo si no existe una previamente
#         if cls._instance is None:
#             cls._instance = super(MongoDBConnection, cls).__new__(cls)
#             cls._instance.session_id = session_id
#             cls._instance.connection_string = os.getenv("MONGO_CONNECTION_STRING")
#             cls._instance.database_name = os.getenv("MONGO_DATABASE_NAME")
#             cls._instance.collection_name = os.getenv("MONGO_COLLECTION_NAME")
#             cls._instance.max_history = 10  # Configura el historial limitado
#             cls._instance.create_index = True  # Configura la creación de índices

#             # Se crea la conexión a la base de datos
#             cls._instance._connection = LimitedMongoDBChatMessageHistory(
#                 session_id=cls._instance.session_id,
#                 connection_string=cls._instance.connection_string,
#                 database_name=cls._instance.database_name,
#                 collection_name=cls._instance.collection_name,
#                 create_index=cls._instance.create_index,
#                 max_history=cls._instance.max_history
#             )
#         return cls._instance

#     def get_connection(self):
#         return self._connection