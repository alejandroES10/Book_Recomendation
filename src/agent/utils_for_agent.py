from abc import ABC, abstractmethod
import sys
import os


from langchain_core.runnables.history import RunnableWithMessageHistory, GetSessionHistoryCallable
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.agents import tool
from langchain.tools.retriever import create_retriever_tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory






sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.ai_models.ollama_client import OllamaClient
from src.database.chroma_database.vector_store import collection_of_books, collection_of_general_information, collection__of__thesis
from langchain_groq import ChatGroq  
from dotenv import load_dotenv
from typing import Callable, List


LLM = OllamaClient().get_llm()

# load_dotenv()
# api_key = os.getenv("GROQ_API_KEY")

# LLM = ChatGroq(temperature=0, model_name="llama-3.1-8b-instant")


@tool
async def get_results(content_to_search: str):
    """Herramienta para buscar libros en el contexto de la biblioteca universitaria.
           Solo puedes recomendar libros o decir si están presentes libros que estén en este contexto, si no son del tema específico que busca el usuario dale los libros similares que aparezcan solo en este contexto.
           Si te preguntan si en la biblioteca hay un libro, y cuando hagas la búsqueda no se encuentra dentro de los resultados, solo di que "no disponen de el libro en la biblioteca, quieres ayuda con otro libro ". 
           Si te preguntan: "Recomiéndame libros que me interesen" revisa su historial de chat a ver qué categorías de libros  ha buscado y recomiéndale libros de esa categoría.
           
            contentToSearch: Lo que el usuario desea buscar, no tiene que ser el input, puede estar en su historial de chat como temas que ya haya buscado

    """
    retriever = collection_of_books.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4},
    )
    return await retriever.abatch([content_to_search])

@tool
async def search_thesis(content_to_search: str):
    """Herramienta para buscar tesis en el contexto de la biblioteca universitaria.
       Solo puedes recomendar tesis o decir si están presentes tesis que estén en este contexto.
       Solo puedes responder preguntas basado en estas tesis y no en tu conocimiento.
       Los metadatos describen características de las tesis como título, autor, y el enlace url.Responde siempre esos metadatos de los fragmentos que recuperes.
       

       content_to_search: El contenido a buscar, puede estar en la consulta o en el historial de chat ejemplo si un usuario te pregunta por una tesis o algo referente a ella de la que viene hablando eso es lo que se pasa en el content to search
      
    """
    retriever = collection__of__thesis.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4},
        
    )
    return await retriever.abatch([content_to_search])



# get_library_information = create_retriever_tool(
#     collection_of_general_information.as_retriever(),
#    "Herramienta para buscar información acerca de los procesos realizados en la biblioteca universitaria",
#     "Se utiliza para buscar información de cómo se realizan los distintos procesos en la biblioteca como por ejemplo el préstamo de libros. No se utiliza para buscar libros ni responder a saludos o presentación del usuario. Si no encuentras resultados di que no disponen de la información")



TOOLS = [get_results, search_thesis]

PROMPT_AGENT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                """Eres un asistente virtual llamado BibCUJAE para información acerca de los libros, tesis e información general existentes en una biblioteca universitaria.
                Responde las preguntas del usuario solo basado en el contexto. 
                Si el contexto no contiene información relevante de las preguntas, no hagas nada y solo di "Solo puedo ayudarte con temas relacionados a la biblioteca".
                No digas respuestas de libros ni tesis basado en tu conocimiento, para eso debes usar las respectivas tools search resul o search tesis
                con el contenido de todo lo que se quiera buscar
               
                """
            ),
            
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)