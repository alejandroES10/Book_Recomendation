
from src.chatbot.agent import agent_with_chat_history


class ChatService :
    
    def get_chat_bot_answer(session_id, input):
        
        return agent_with_chat_history.invoke(
            {"input": f"{input}"},
            # This is needed because in most real world scenarios, a session id is needed
            # It isn't really used here because we are using a simple in memory ChatMessageHistory
            config={"configurable": {"session_id": {session_id}}},
)
