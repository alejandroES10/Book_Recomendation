from typing import List
from langchain_core.messages import BaseMessage
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
from datetime import datetime

# class LimitedMongoDBChatMessageHistory(MongoDBChatMessageHistory):
#     def __init__(self, *args, max_history: int = 10, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.max_history = max_history
    
#     def add_messages(self, messages: List[BaseMessage]) -> None:
#         for message in messages:
#             # Solo guardar lo esencial
#             message.additional_kwargs = {
#                 "timestamp": datetime.utcnow().isoformat()
#             }
            
#             # Eliminar campos innecesarios
#             for attr in ["response_metadata", "name", "id", "example", 
#                         "invalid_tool_calls", "usage_metadata","tool_calls"]:
#                 if hasattr(message, attr):
#                     delattr(message, attr)
        
#         super().add_messages(messages)
        
#         # Mantener límite de historial
#         if len(self.messages) > self.max_history:
#             self.clear()
#             super().add_messages(self.messages[-self.max_history:])




# class LimitedMongoDBChatMessageHistory(MongoDBChatMessageHistory):
#     def __init__(self, *args, max_history: int = 10, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.max_history = max_history
    
#     async def aadd_messages(self, messages: List[BaseMessage]) -> None:
#         # Agregar timestamp a cada mensaje
#         for message in messages:
#             if not hasattr(message, 'additional_kwargs'):
#                 message.additional_kwargs = {}
#             message.additional_kwargs['timestamp'] = datetime.now().isoformat()
 
     
#         await super().aadd_messages(messages)
#         all_messages = super().messages
        
#         if len(all_messages) > self.max_history:
#             last_messages = all_messages[-self.max_history:]
#             await self.aclear()
#             super().aadd_messages(last_messages)

import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# class MongoClientSingleton:
#     _client = None

#     @classmethod
#     def get_client(cls) -> MongoClient:
#         if cls._client is None:
#             cls._client = MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
#         return cls._client

from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class MongoClientSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoClientSingleton, cls).__new__(cls)
            cls._instance._client = MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
        return cls._instance

    def get_client(self) -> MongoClient:
        return self._client




class LimitedMongoDBChatMessageHistory(MongoDBChatMessageHistory):
    def __init__(self, session_id: str, database_name: str, collection_name: str, **kwargs):
        # Obtener el cliente singleton
        client = MongoClientSingleton.get_client()
        self.client = client  # Inyectar cliente singleton
        self.session_id = session_id
        self.database_name = database_name
        self.collection_name = collection_name
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

        self.session_id_key = kwargs.get("session_id_key", "session_id")
        self.history_key = kwargs.get("history_key", "history")
        self.history_size = kwargs.get("history_size", None)

        if kwargs.get("create_index", True):
            self.collection.create_index(self.session_id_key, **kwargs.get("index_kwargs", {}))

        self.max_history = kwargs.get("max_history", 10)

    async def aadd_messages(self, messages: List[BaseMessage]) -> None:
        for message in messages:
            if not hasattr(message, 'additional_kwargs'):
                message.additional_kwargs = {}
            message.additional_kwargs['timestamp'] = datetime.now().isoformat()

        await super().aadd_messages(messages)
        all_messages = super().messages

        if len(all_messages) > self.max_history:
            last_messages = all_messages[-self.max_history:]
            await self.aclear()
            super().aadd_messages(last_messages)