from langchain.tools.retriever import create_retriever_tool

from src.database.vector_store import  collection__of__books

retriever_of_books = collection__of__books.as_retriever()

tool_for_search_book = create_retriever_tool(retriever_of_books,"herramienta para buscar libros de la biblioteca","herramienta para buscar libros de la biblioteca así como hacer recomendaciones, si no aparece el libro que se busca devolver temas relacionados a la búsqueda")