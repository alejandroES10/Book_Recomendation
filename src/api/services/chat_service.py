
from src.chatbot.agent import agent_with_chat_history, get_answer
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory


class ChatService :
    
    def delete_chat_history(session_id):

        chat_history = MongoDBChatMessageHistory(
            session_id=session_id,
            connection_string="mongodb://localhost:27017",
            database_name="my_db",
            collection_name="chat_histories",
        )
     
        return chat_history.clear()
        

    def get_chat_history(session_id):
        chat_history = MongoDBChatMessageHistory(
            session_id=session_id,
            connection_string="mongodb://localhost:27017",
            database_name="my_db",
            collection_name="chat_histories",
        )
         
        return chat_history.messages
    
    
    def get_chat_bot_answer(session_id, input):  
        return get_answer(session_id, input)

