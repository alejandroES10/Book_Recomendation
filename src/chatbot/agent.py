


import sys
import os


from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.agents import tool
from langchain.tools.retriever import create_retriever_tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.ollama.ollama_llm import llm
from src.database.vector_store import collection__of__books, collection__of__general_information    



@tool
async def get_results(content_to_search: str, k_results: int):
    """Herramienta para buscar libros en la biblioteca universitaria.

    Solo puedes recomendar libros o indicar si están disponibles.
    Si el libro no está en la biblioteca, responde: "No disponemos del libro 
    en la biblioteca,¿quieres ayuda con otro libro?".Si el usuario solicita 
    recomendaciones, revisa su historial de chat y sugiere libros de categorías 
    previas.

    content_to_search: El input del usuario.
    k_results:La cantidad de resultados que se quiere, por defecto 4 siempre.

    """
    retriever = collection__of__books.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k_results},
    )
    return await retriever.abatch([content_to_search])


get_library_information = create_retriever_tool(
    collection__of__general_information.as_retriever(),
    name="Herramienta para buscar información sobre la biblioteca universitaria",
    description=(
        """Herramienta para buscar información acerca de los procesos realizados en la 
        biblioteca universitaria. Se utiliza para buscar información de cómo se realizan 
        los distintos procesos en la biblioteca como por ejemplo el préstamo de libros. 
        No se utiliza para buscar libros ni responder a saludos o presentación del usuario
        """
    ),
)

tools = [get_results, get_library_information]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                """Eres un asistente virtual llamado BibCUJAE para información sobre
                los libros en una biblioteca universitaria.
                Responde solo con información basada en la base de datos.
                Si un usuario te saluda, responde el saludo sin usar herramientas.
                Si un usuario se presenta y saluda, puedes responderle.
                Si la pregunta no tiene contexto en la base de datos, responde:
                Solo puedo ayudarte con temas relacionados a la biblioteca.
                """
            ),
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools,  verbose=True)
from typing import List
from langchain_core.messages import BaseMessage

class LimitedMongoDBChatMessageHistory(MongoDBChatMessageHistory):
    def __init__(self, *args, max_history: int = 10, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_history = max_history
    
    def add_messages(self, messages: List[BaseMessage]) -> None:
        super().add_messages(messages)
        all_messages = super().messages  # Obtener todos los mensajes
        if len(all_messages) > self.max_history:
            # Mantener solo los últimos `max_history` mensajes
            last_messages = all_messages[-self.max_history:]
            self.clear()  # Borrar todo el historial
            super().add_messages(last_messages)  # Guardar solo los últimos N

# Configuración del agente con historial limitado
agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: LimitedMongoDBChatMessageHistory(
        session_id=session_id,
        connection_string="mongodb://localhost:27017",
        database_name="chats_db",
        collection_name="chat_histories",
        max_history=10  # Físicamente limita a 6 mensajes en MongoDB
    ),
    input_messages_key="question",
    history_messages_key="history",
)

# agent_with_chat_history = RunnableWithMessageHistory(
#     agent_executor,
#     lambda session_id: MongoDBChatMessageHistory(
#         session_id=session_id,
#         connection_string="mongodb://localhost:27017",
#         database_name="chats_db",
#         collection_name="chat_histories",
#         history_size= 6
#     ),
#     input_messages_key="question",
#     history_messages_key="history",
# )


async def get_answer(session_id: str, user_input: str):
    """Obtiene la respuesta del agente basado en el historial de chat.

    Args:
        session_id (str): ID de la sesión del usuario.
        user_input (str): Entrada del usuario.

    Returns:
        dict: Respuesta del agente.
    """
    

    return await agent_with_chat_history.ainvoke(
        {"question": user_input} or {},
        config={"configurable": {"session_id": session_id}},
    )

