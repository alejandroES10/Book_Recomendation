from typing import List
from langchain_core.messages import BaseMessage
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
from src.api.interfaces.ichat_service import IChatService
from src.chatbot.agent import get_answer
from src.database.mongodb.limited_mongodb_chat_message_history import LimitedMongoDBChatMessageHistory
from src.api.models.message_model import MessageModel
from src.api.models.chat_history_model import ChatHistoryModel
import os
from dotenv import load_dotenv

from src.database.mongodb.mongodb_connection import MongoDBConnection
from src.database.postgres.chats.postgres_chats import BaseChatWithDatabase, ChatWithPostgres
from langchain_core.chat_history import BaseChatMessageHistory

class ChatService (IChatService):
    
    def __init__(self):
        self._chat_with_database = ChatWithPostgres()
        

    #********* BaseChatMessageHistory *********
    
    # async def _build_chat_history(session_id: str) -> MongoDBChatMessageHistory:
    #     """Create and return a MongoDB chat history instance"""

    #     return MongoDBConnection.get_connection(session_id)

        # return await chat.aget_messages()
        
    async def _build_chat_history(self,session_id: str) -> BaseChatMessageHistory:
        """Create and return a MongoDB chat history instance"""

        return self._chat_with_database.get_chat_history(session_id)

   
    async def delete_chat_history(self, session_id: str) -> None:
        """Delete chat history for a session"""
        chat_history = await self._build_chat_history(session_id)
        if not chat_history.messages:
            raise ValueError(f"No chat history found for session: {session_id}")
        await chat_history.aclear()

    
    async def get_chat_history(self,session_id: str) -> ChatHistoryModel:
        """Retrieve chat history for a session"""
        chat_history = await  self._build_chat_history(session_id)
        if not chat_history.messages:
            raise ValueError(f"No chat history found for session: {session_id}")
        
        history = [
            MessageModel(
                type=msg.type,
                content=msg.content,
                created_at=msg.additional_kwargs.get("timestamp") if msg.additional_kwargs else None
            )
            for msg in chat_history.messages
        ]

        return ChatHistoryModel(session_id=session_id, history=history)
    
    
    
    async def get_chat_bot_answer(self,session_id: str, input: str) -> str:
        """Get chatbot response for user input"""
        
        try:
            return await get_answer(session_id, input)
        except Exception as e:
            raise ValueError(f"Failed to get chatbot answer: {str(e)}")


