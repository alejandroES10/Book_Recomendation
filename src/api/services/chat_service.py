from typing import List
from langchain_core.messages import BaseMessage
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
from src.api.interfaces.ichat_service import IChatService

from src.database.mongodb.limited_mongodb_chat_message_history import LimitedMongoDBChatMessageHistory
from src.api.models.message_model import MessageModel
from src.api.models.chat_history_model import ChatHistoryModel
import os
from dotenv import load_dotenv

from src.database.mongodb.mongodb_connection import MongoDBConnection
from src.database.postgres.chats.custom_sql_chat_message_history import CustomSQLChatMessageHistory
from src.database.postgres.chats.postgres_chats import BaseChatWithDatabase, ChatWithPostgres
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from src.chatbot.agent import AgentChatBot


class ChatService (IChatService):
    
    def __init__(self):
        self._chat_with_database = ChatWithPostgres()
        self._agent = AgentChatBot()
        

    #********* BaseChatMessageHistory *********
    
    # async def _build_chat_history(session_id: str) -> MongoDBChatMessageHistory:
    #     """Create and return a MongoDB chat history instance"""

    #     return MongoDBConnection.get_connection(session_id)

        # return await chat.aget_messages()
        
    def build_chat_history(self,session_id: str) -> CustomSQLChatMessageHistory:
        """Create and return a SQL chat history instance"""

        return self._chat_with_database.get_chat_history(session_id)

   
    async def delete_chat_history(self, session_id: str) -> None:
        """Delete chat history for a session"""
        chat_history = self.build_chat_history(session_id)
        if not chat_history.messages:
            raise ValueError(f"No chat history found for session: {session_id}")
        await chat_history.aclear()

    
    async def get_chat_history(self,session_id: str):
        """Retrieve chat history for a session"""
        chat_history = self.build_chat_history(session_id)
        history = await chat_history. aget_raw_messages()
        if not history:
            raise ValueError(f"No chat history found for session: {session_id}")
        
        # history = [
        #     MessageModel(
        #         type=msg.type,
        #         content=msg.content,
        #         created_at=msg.additional_kwargs.get("timestamp") if msg.additional_kwargs else None
        #     )
        #     for msg in chat_history.messages
        # ]

        # return ChatHistoryModel(session_id=session_id, history=history)

        return history
    
    
    
    async def get_chat_bot_answer(self,session_id: str, input: str) -> str:
        
        """Get chatbot response for user input"""
        
        try:
            
            result = await self._agent.get_answer(session_id, input,self.build_chat_history)
            if not result:
                raise ValueError("No response from chatbot")
            response = {"ouput": result['output'] }
            return response
        except Exception as e:
            raise ValueError(f"Failed to get chatbot answer: {str(e)}")


