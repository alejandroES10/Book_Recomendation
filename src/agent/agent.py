


from abc import ABC, abstractmethod
import sys
import os


from langchain_core.runnables.history import RunnableWithMessageHistory, GetSessionHistoryCallable
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.agents import tool
from langchain.tools.retriever import create_retriever_tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder




sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.ai_models.ollama_client import OllamaClientSingleton
from src.database.chroma_database.vector_store import collection_of_books, collection_of_general_information, collection__of__thesis
from langchain_groq import ChatGroq  
from dotenv import load_dotenv
from typing import Callable, List
from src.agent.utils_for_agent import TOOLS, PROMPT_AGENT, LLM



from langchain_core.chat_history import BaseChatMessageHistory

class Agent(ABC):
    @abstractmethod
    async def get_answer(self, session_id: str, user_input: str, chat_history: GetSessionHistoryCallable):
        """Obtiene la respuesta del agente basado en el historial de chat."""
        pass


class AgentChatBot(Agent):
    def __init__(self):
        self.llm = LLM
        self.tools = TOOLS
        self.prompt = PROMPT_AGENT
        self.agent_executor = self._create_agent_executor()

    def _create_agent_executor(self) -> AgentExecutor:
        agent = self._create_agent()
        return AgentExecutor(agent=agent, tools=self.tools, verbose=True)

    def _create_agent(self):
        return create_tool_calling_agent(self.llm, self.tools, self.prompt)

    async def get_answer(self, session_id: str, user_input: str, get_chat_history: GetSessionHistoryCallable):
        """Ejecuta el agente con historial de chat inyectado."""
        agent_with_chat_history = RunnableWithMessageHistory(
            self.agent_executor,
            lambda session_id: get_chat_history(session_id),
            input_messages_key="question",
            history_messages_key="history",
        )

        return await agent_with_chat_history.ainvoke(
            {"question": user_input},
            config={"configurable": {"session_id": session_id}}
        )