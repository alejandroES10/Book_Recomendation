from typing import List
from langchain_core.messages import BaseMessage
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
from datetime import datetime






class LimitedMongoDBChatMessageHistory(MongoDBChatMessageHistory):
    def __init__(self, *args, max_history: int = 10, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_history = max_history
    
    def add_messages(self, messages: List[BaseMessage]) -> None:
        # Agregar timestamp a cada mensaje
        for message in messages:
            if not hasattr(message, 'additional_kwargs'):
                message.additional_kwargs = {}
            message.additional_kwargs['timestamp'] = datetime.utcnow().isoformat()  # Fecha en formato ISO
        
        super().add_messages(messages)
        all_messages = super().messages
        
        if len(all_messages) > self.max_history:
            last_messages = all_messages[-self.max_history:]
            self.clear()
            super().add_messages(last_messages)