from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.ollama.ollama_llm import llm
from src.database.vector_store import collection__of__books
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.chatbot.tools_for_agent import tool_for_search_book
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from src.database.vector_store import collection__of__general_information



from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.agents import tool
from langchain.tools.retriever import create_retriever_tool
from langchain_core.prompts import ChatPromptTemplate

from langchain_core.prompts import MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory

@tool
def get_results(contentToSearch: str, k_results: int):
        """Herramienta para buscar libros en el contexto de la biblioteca universitaria.
           Solo puedes recomendar libros o decir si están presentes libros que estén en este contexto.
           Si te preguntan si en la biblioteca hay un libro, y cuando hagas la búsqueda no se encuentra dentro de los resultados, solo di que "no disponen de el libro en la biblioteca, quieres ayuda con otro libro ". 
           Si te preguntan: "Recomiéndame libros que me interesen" revisa su historial de chat a ver qué categorías de libros  ha buscado y recomiéndale libros de esa categoría.
           
            contentToSearch: El input del usuario
            k_results: la cantidad de resultados que se quiere, por defecto 4 siempre
        """
        retriever = collection__of__books.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k_results},
        ) 
        
        return retriever.batch([contentToSearch])


    
get_library_information = create_retriever_tool(collection__of__general_information.as_retriever(),"Herramienta para buscar información acerca de los procesos realizados en la biblioteca universitaria",
                                             "Se utiliza para buscar información de cómo se realizan los distintos procesos en la biblioteca como por ejemplo el préstamo de libros. No se utiliza para buscar libros ni responder a saludos o presentación del usuario")


tools = [get_results,get_library_information]


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
        Eres un asistente virtual llamado BibCUJAE para información acerca de los libros existentes en una biblioteca universitaria.
        Responde las preguntas del usuario solo basado en el contexto. 
        Si un usuario te saluda le respondes el saludo.
        Si un usuario se presenta con su nombre y te saluda puedes responderle.
        Si el contexto no contiene información relevante de las preguntas, no hagas nada y solo di "Solo puedo ayudarte con temas relacionados a la biblioteca".
        No uses ningún conocimiento que no provenga directamente de la base de datos.
        

""",
        ),
        MessagesPlaceholder(variable_name="history"), #chat_history de la otra forma
        ("human", "{question}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)



agent = create_tool_calling_agent(llm, tools, prompt )


agent_executor = AgentExecutor(agent=agent, tools = tools, verbose=True)


# chat_message_history = MongoDBChatMessageHistory(
#     session_id="test_session",
#     connection_string="mongodb://localhost:27017",
#     database_name="my_db",
#     collection_name="chat_histories",
# )


agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: MongoDBChatMessageHistory(
        session_id=session_id,
        connection_string="mongodb://localhost:27017",
        database_name="my_db",
        collection_name="chat_histories",
    ),
    input_messages_key="question",
    history_messages_key="history",
)


