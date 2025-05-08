


import sys
import os


from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.agents import tool
from langchain.tools.retriever import create_retriever_tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.database.mongodb.mongodb_connection import MongoDBConnection
from src.ollama.ollama_client import OllamaClientSingleton
from src.database.vector_store import collection_of_books, collection_of_general_information, collection__of__thesis
from langchain_groq import ChatGroq  
from dotenv import load_dotenv
from typing import List
from src.database.mongodb.limited_mongodb_chat_message_history import LimitedMongoDBChatMessageHistory

# llm = OllamaClientSingleton().get_llm()

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatiles")


@tool
async def get_results(content_to_search: str, k_results: int):
    """Herramienta para buscar libros en el contexto de la biblioteca universitaria.
           Solo puedes recomendar libros o decir si están presentes libros que estén en este contexto, si no son del tema específico que busca el usuario dale los libros similares que aparezcan solo en este contexto.
           Si te preguntan si en la biblioteca hay un libro, y cuando hagas la búsqueda no se encuentra dentro de los resultados, solo di que "no disponen de el libro en la biblioteca, quieres ayuda con otro libro ". 
           Si te preguntan: "Recomiéndame libros que me interesen" revisa su historial de chat a ver qué categorías de libros  ha buscado y recomiéndale libros de esa categoría.
           
            contentToSearch: El input del usuario
            k_results: la cantidad de resultados que se quiere, por defecto 4 siempre
    """
    retriever = collection_of_books.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k_results},
    )
    return await retriever.abatch([content_to_search])

@tool
async def search_thesis(content_to_search: str):
    """Herramienta para buscar tesis en el contexto de la biblioteca universitaria.
       Solo puedes recomendar tesis o decir si están presentes tesis que estén en este contexto.
       Solo puedes responder preguntas basado en estas tesis y no en tu conocimiento.
       Los metadatos describen características de las tesis como título, autor, y el enlace url.Responde siempre esos metadatos de los fragmentos que recuperes.
       Cuando devuelvas el enlace deja un espacio para que desde el front se le de clic y se acceda.
       Debes responder preguntas sobre las tesis que te pregunten. 
       No des información de identificadores de tesis (id), si te preguntan di que no tienes esa información.
       Si no son del tema específico que busca el usuario, ofrece las tesis similares que aparezcan solo en este contexto.
       Si te preguntan si en la biblioteca hay una tesis, y no se encuentra entre los resultados, di: 
       "No disponemos de esa tesis en la biblioteca. ¿Quieres ayuda con otra tesis?"
       Si te preguntan: "Recomiéndame tesis que me interesen", revisa su historial de chat para ver qué temas ha buscado y recomiéndale tesis relacionadas.

       content_to_search: El contenido a buscar
      
    """
    retriever = collection__of__thesis.as_retriever(
        search_type="similarity",
        
    )
    return await retriever.abatch([content_to_search])



# get_results = create_retriever_tool(
#     collection__of__books.as_retriever(),
#     name="Herramienta para buscar libros en la biblioteca universitaria",
#     description=(
#         """Herramienta para buscar libros en la biblioteca universitaria. 
#         Solo puedes recomendar libros o indicar si están disponibles. 
#         Si el libro no está en la biblioteca, responde: 'No disponemos del libro en la biblioteca,¿quieres ayuda con otro libro?'
#         Si el usuario solicita recomendaciones, revisa su historial de chat y sugiere libros de categorías previas.
#         """
#     ),
# )

get_library_information = create_retriever_tool(
    collection_of_general_information.as_retriever(),
   "Herramienta para buscar información acerca de los procesos realizados en la biblioteca universitaria",
    "Se utiliza para buscar información de cómo se realizan los distintos procesos en la biblioteca como por ejemplo el préstamo de libros. No se utiliza para buscar libros ni responder a saludos o presentación del usuario. Si no encuentras resultados di que no disponen de la información")

# get_tesis_information = create_retriever_tool(
#     collection__of__thesis.as_retriever(),
#    "Herramienta para buscar información acerca de las tesis realizadas en la universidad",
#     "Se utiliza para buscar información sobre las distintas tesis realizadas en la universidad. No se utiliza para buscar libros ni responder a saludos o presentación del usuario")


tools = [get_results, get_library_information,search_thesis]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                """Eres un asistente virtual llamado BibCUJAE para información acerca de los libros existentes en una biblioteca universitaria.
                Responde las preguntas del usuario solo basado en el contexto. 
                Si un usuario te saluda le respondes el saludo.
                Si un usuario se presenta con su nombre y te saluda puedes responderle.
                Si el contexto no contiene información relevante de las preguntas, no hagas nada y solo di "Solo puedo ayudarte con temas relacionados a la biblioteca".
                No uses ningún conocimiento que no provenga directamente de la base de datos.
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








# Configuración del agente con historial limitado
# agent_with_chat_history = RunnableWithMessageHistory(
#     agent_executor,
#     lambda session_id: LimitedMongoDBChatMessageHistory(
#         session_id=session_id,
#         connection_string="mongodb://localhost:27017",
#         database_name="chats_db",
#         collection_name="chat_histories",
#         create_index=True,
#         max_history=10  # Físicamente limita a 6 mensajes en MongoDB
#     ),
#     input_messages_key="question",
#     history_messages_key="history",
# )

# import os

# agent_with_chat_history = RunnableWithMessageHistory(
#     agent_executor,
#     lambda session_id: LimitedMongoDBChatMessageHistory(
#         session_id=session_id,
#         connection_string=os.environ["MONGO_CONNECTION_STRING"],  
#         database_name=os.environ["MONGO_DATABASE_NAME"],  
#         collection_name=os.environ["MONGO_COLLECTION_NAME"], 
#         create_index=True,
#         max_history=10 
#     ),
#     input_messages_key="question",
#     history_messages_key="history",
# )



agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: MongoDBConnection.get_connection(session_id),
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
        {"question": user_input},
        config={"configurable": {"session_id": session_id}},
    )

