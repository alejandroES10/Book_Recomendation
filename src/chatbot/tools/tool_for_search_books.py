from langchain.tools.retriever import create_retriever_tool
from retrievers.retriever_of_books import retriever_of_books

tool_for_search_book = create_retriever_tool(retriever_of_books,"herramienta para buscar libros de la biblioteca","herramienta para buscar libros de la biblioteca así como hacer recomendaciones")