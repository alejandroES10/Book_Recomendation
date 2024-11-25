from langchain.tools.retriever import create_retriever_tool

from src.database.vector_store import  collection__of__books

retriever_of_books = collection__of__books.as_retriever()

tool_for_search_book = create_retriever_tool(retriever_of_books,"herramienta para buscar libros de la biblioteca universitaria","herramienta para buscar libros de la biblioteca universitaria así como hacer recomendaciones, el title es el título, el page content es la descripción")
