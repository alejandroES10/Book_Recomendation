from langchain.tools.retriever import create_retriever_tool

from src.database.chromadb.vector_store import  collection__of__books

retriever_of_books = collection__of__books.as_retriever(search_type="similarity")
retriever_of_books.search_kwargs = {"include_metadata": True}

tool_for_search_book = create_retriever_tool(retriever_of_books,"herramienta para buscar libros de la biblioteca universitaria",
                                             "herramienta para buscar libros de la biblioteca universitaria así como hacer recomendaciones, Utiliza los metadatos de los libros para saber sus respectivos títulos y autores. Solo puedes recomendar libros que se encuentren aquí")
