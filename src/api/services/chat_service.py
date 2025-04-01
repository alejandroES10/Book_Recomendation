from typing import List
from langchain_core.messages import BaseMessage
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
from src.chatbot.agent import agent_with_chat_history, get_answer

class ChatService:
    @staticmethod
    def _get_chat_history(session_id: str) -> MongoDBChatMessageHistory:
        """Create and return a MongoDB chat history instance"""
        return MongoDBChatMessageHistory(
            session_id=session_id,
            connection_string="mongodb://localhost:27017",
            database_name="library_db",
            collection_name="chat_histories",
        )

    @staticmethod
    async def delete_chat_history(session_id: str) -> None:
        """Delete chat history for a session"""
        chat_history = ChatService._get_chat_history(session_id)
        if not chat_history.messages:
            raise ValueError(f"No chat history found for session: {session_id}")
        chat_history.clear()

    @staticmethod
    async def get_chat_history(session_id: str) -> List[BaseMessage]:
        """Retrieve chat history for a session"""
        chat_history = ChatService._get_chat_history(session_id)
        if not chat_history.messages:
            raise ValueError(f"No chat history found for session: {session_id}")
        return chat_history.messages

    @staticmethod
    async def get_chat_bot_answer(session_id: str, input: str) -> str:
        """Get chatbot response for user input"""
        try:
            return await get_answer(session_id, input)
        except Exception as e:
            raise ValueError(f"Failed to get chatbot answer: {str(e)}")