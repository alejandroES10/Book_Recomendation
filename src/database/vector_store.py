from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from src.ollama.ollama_embeddings import embedding_function
import chromadb
# from langchain_ollama import OllamaEmbeddings
# from langchain_community.chat_models import ChatOllama
import asyncio
 
persistent_client = chromadb.PersistentClient()

# collection_of_books_ = persistent_client.get_or_create_collection("collection_of_books_",embedding_function= embedding_function)

collection__of__books = Chroma(
    client=persistent_client,
    collection_name="collection__of__books",
    embedding_function=embedding_function,
    
)

# file_path = "./files/Procesos-realizados-en-la-biblioteca-universitaria.pdf"


from langchain_community.document_loaders import PyPDFLoader


# async def load():
#         loader = PyPDFLoader("/Users/alejandroestrada/Documents/Procesos realizados en la biblioteca universitaria.pdf")
#         pages = loader.load()
    
        # async for page in loader.alazy_load():
        #   pages.append(page)
          
        # return pages

loader = PyPDFLoader("/Users/alejandroestrada/Documents/Procesos realizados en la Biblioteca Universitaria .pdf")
pages = loader.load()


library_information = Chroma.from_documents(
    documents=pages,
    embedding=embedding_function,
    persist_directory="./files"
    )

# library_information = Chroma(
#     client= persistent_client,
#     collection_name= "library_information",
#     embedding_function=embedding_function
# )

# documents = [
#     Document(
#         page_content="Los perros son excelentes compañeros, conocidos por su lealtad y amabilidad.",
#         metadata={"source": "documento-mamiferos-mascotas"},
#         id="1"
        
#     ),
#     Document(
#         page_content="Los gatos son mascotas independientes que a menudo disfrutan de su propio espacio.",
#         metadata={"source": "documento-mamiferos-mascotas"},
#         id = "2"
#     ),
#     Document(
#         page_content="Los peces dorados son mascotas populares para principiantes, ya que requieren un cuidado relativamente simple.",
#         metadata={"source": "documento-peces-mascotas"},
#         id="3"
#     ),
#     Document(
#         page_content="Los loros son aves inteligentes capaces de imitar el habla humana.",
#         metadata={"source": "documento-aves-mascotas"},
#         id="4"
#     ),
#     Document(
#         page_content="Los conejos son animales sociales que necesitan mucho espacio para saltar.",
#         metadata={"source": "documento-mamiferos-mascotas"},
#         id="5"
#     ),
# ]

# collection_of_books.add(documents= documents, ids=["1","2","3","4","5"])


# vectorstore_of_books = Chroma(
#     client=persistent_client,
#     collection_name= "collection_of_books",
#     embedding_function=embedding_function,
# )

# vectorstore_of_books_ = Chroma.from_documents(
#     documents= documents,
#     ids=["1","2","3","4","5"],
#     embedding= embedding_function
# )

# vectorstore_of_books.delete_collection()

# vectorstore_of_thesis = Chroma.from_documents(
#     documents= [],
#     ids=[],
#     embedding= embedding_function
# )

