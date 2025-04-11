from abc import ABC, abstractmethod
from langchain_core.messages import BaseMessage
from typing import List


class MessageStrategy(ABC):
    @abstractmethod
    def apply(self, messages: List[BaseMessage]) -> List[BaseMessage]:
        pass


from datetime import datetime

class CleanMessageStrategy(MessageStrategy):
    def apply(self, messages: List[BaseMessage]) -> List[BaseMessage]:
        for msg in messages:
            msg.additional_kwargs = {
                "timestamp": datetime.utcnow().isoformat()
            }
            for attr in ["response_metadata", "name", "id", "example", 
                         "invalid_tool_calls", "usage_metadata"]:
                if hasattr(msg, attr):
                    delattr(msg, attr)
        return messages

class LimitHistoryStrategy(MessageStrategy):
    def __init__(self, max_history: int = 10):
        self.max_history = max_history

    def apply(self, messages: List[BaseMessage]) -> List[BaseMessage]:
        return messages[-self.max_history:]

from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory

class StrategicMongoDBChatMessageHistory(MongoDBChatMessageHistory):
    def __init__(self, *args, strategies: List[MessageStrategy] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.strategies = strategies or []

    def add_messages(self, messages: List[BaseMessage]) -> None:
        # Aplica cada estrategia secuencialmente
        for strategy in self.strategies:
            messages = strategy.apply(messages)

        # Almacena los mensajes procesados
        super().add_messages(messages)

        # Aplica limitación si las estrategias no lo hacen internamente
        if len(self.messages) > 100:  # Resguardo general
            self.clear()
            super().add_messages(self.messages[-100:])



# agent_with_chat_history = RunnableWithMessageHistory(
#     agent_executor,
#     lambda session_id: StrategicMongoDBChatMessageHistory(
#         session_id=session_id,
#         connection_string="mongodb://localhost:27017",
#         database_name="chats_db",
#         collection_name="chat_histories",
#         strategies=[
#             CleanMessageStrategy(),
#             LimitHistoryStrategy(max_history=10)
#         ]
#     ),
#     input_messages_key="question",
#     history_messages_key="history",
# )
