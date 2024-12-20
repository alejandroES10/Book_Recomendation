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
from src.database.vector_store import library_information

# memory = MemorySaver()
# # message = SystemMessage(content=              """
# #         Eres un asistente virtual llamado Alejandro para información acerca de los libros existentes en una biblioteca universitaria.
# #         Responde las preguntas del usuario solo basado en el contexto. 
# #         Si el contexto no contiene información relevante de las preguntas, no hagas nada y solo di "Solo puedo ayudarte con temas relacionados a la biblioteca"
# #  """)
# agent_executor = create_react_agent(llm, tools=[tool_for_search_book], checkpointer=memory)

# config = {"configurable": {"thread_id": "abc123"}}

# for s in agent_executor.stream(
#     {"messages": [HumanMessage(content="Hola")]}, config=config
# ):
#     print(s)
#     print("----")

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.agents import tool
from langchain.tools.retriever import create_retriever_tool

@tool
def get_results(contentToSearch: str, k_results: int):
        """Herramienta para buscar libros en el contexto de la biblioteca universitaria.
           Solo puedes recomendar libros o decir si están presentes libros que estén en este contexto. 
        Args:
            contentToSearch: El input del usuario
            k_results: la cantidad de resultados que se quiere, por defecto 4 siempre
        """
        retriever = collection__of__books.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k_results},
        ) 
        
        return retriever.batch([contentToSearch])

# @tool
# def get_library_information(contentToSearch: str):
#         """Herramienta para buscar información acerca de los procesos realizados en la biblioteca universitaria por ejemplo los préstamos de libros.
            
#         Args:
#             contentToSearch: El input del usuario que quiere saber
#         """
#         retriever = library_information.as_retriever(
#             search_type="similarity",
#         ) 
        
#         return retriever.batch([contentToSearch])
    
get_library_information = create_retriever_tool(library_information.as_retriever(),"Herramienta para buscar información acerca de los procesos realizados en la biblioteca universitaria",
                                             "Se utiliza para buscar información de cómo se realizan los distintos procesos en la biblioteca como por ejemplo el préstamo de libros. No se utiliza para buscar libros ni responder a saludos o presentación del usuario")


tools = [get_results,get_library_information]

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.prompts import MessagesPlaceholder

# prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             """
#         Eres un asistente virtual llamado Alejandro para información acerca de los libros existentes en una biblioteca universitaria.
#         Responde las preguntas del usuario solo basado en el contexto. 
#         Si un usuario se presenta con su nombre y te saluda puedes responderle.
#         Si el contexto no contiene información relevante de las preguntas, no hagas nada y solo di "Solo puedo ayudarte con temas relacionados a la biblioteca"

# """,
#         ),
#         ("user", "{input}"),
#         MessagesPlaceholder(variable_name="agent_scratchpad"),
#     ]
# )

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
        Eres un asistente virtual llamado Alejandro para información acerca de los libros existentes en una biblioteca universitaria.
        Responde las preguntas del usuario solo basado en el contexto. 
        Si un usuario se presenta con su nombre y te saluda puedes responderle.
        Si el contexto no contiene información relevante de las preguntas, no hagas nada y solo di "Solo puedo ayudarte con temas relacionados a la biblioteca.
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

# store = {}

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory

chat_message_history = MongoDBChatMessageHistory(
    session_id="test_session",
    connection_string="mongodb://localhost:27017",
    database_name="my_db",
    collection_name="chat_histories",
)

chat_message_history.add_user_message("Hello")
chat_message_history.add_ai_message("Hi")
# def get_session_history(session_id: str) -> BaseChatMessageHistory:
#     if session_id not in store:
#         store[session_id] = ChatMessageHistory()
#     return store[session_id]
# message_history = ChatMessageHistory()
# agent_with_chat_history = RunnableWithMessageHistory(
#     agent_executor,
#     # This is needed because in most real world scenarios, a session id is needed
#     # It isn't really used here because we are using a simple in memory ChatMessageHistory
#     # get_session_history,
#     lambda session_id: message_history,
#     input_messages_key="input",
#     history_messages_key="chat_history",
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

# agent_with_chat_history.invoke(
#     {"input": "hola cuál te dije que era mi nombre?"},
#     # This is needed because in most real world scenarios, a session id is needed
#     # It isn't really used here because we are using a simple in memory ChatMessageHistory
#     config={"configurable": {"session_id": "123"}},
# )

# agent_executor.invoke(
#     {
#         "input": "Tienen libros de Stuart Russell y Peter Norvig ?" 
#     },
    
# )