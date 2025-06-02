from typing import List
from langchain_core.messages import BaseMessage
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
from src.interfaces.ichat_service import IChatService


from src.schemas.message_schema import MessageSchema
from src.schemas.chat_history_schema import ChatHistorySchema
import os
from dotenv import load_dotenv


from src.database.postgres_database.chats.custom_sql_chat_message_history import CustomSQLChatMessageHistory
from src.database.postgres_database.chats.chats_repository import  BaseChatWithDatabase, ChatWithPostgres
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from src.chatbot.agent import Agent


class ChatService (IChatService):
    
    def __init__(self, chat_with_database:BaseChatWithDatabase, agent: Agent):
        self._chat_with_database = chat_with_database
        self._agent = agent
        
        
    def build_chat_history(self,session_id: str) -> CustomSQLChatMessageHistory:
        """Create and return a SQL chat history instance"""

        return self._chat_with_database.get_chat_history(session_id)

   
    async def delete_chat_history(self, session_id: str) -> None:
        """Delete chat history for a session"""
        chat_history = self.build_chat_history(session_id)
        messages = await chat_history.aget_messages()
        if len(messages) == 0:
            raise ValueError(f"No chat history found for session: {session_id}")
        await chat_history.aclear()

    
    async def get_chat_history(self,session_id: str):
        """Retrieve chat history for a session"""
        chat_history = self.build_chat_history(session_id)
        history = await chat_history.aget_raw_messages()
        if not history:
            raise ValueError(f"No chat history found for session: {session_id}")
        

        return history
    
    
    
    async def get_chat_bot_answer(self,session_id: str, input: str) -> str:
        
        """Get chatbot response for user input"""
        
        try:
            
            result = await self._agent.get_answer(session_id, input,self.build_chat_history)
            if not result:
                raise ValueError("No response from chatbot")
            response = {"output": result['output'] }
            return response
        except Exception as e:
            raise ValueError(f"Failed to get chatbot answer: {str(e)}")


