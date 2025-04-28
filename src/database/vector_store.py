# from langchain_core.documents import Document
# from langchain_chroma import Chroma
# from langchain_community.embeddings import OllamaEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from src.ollama.ollama_embeddings import embedding_function
# import chromadb
# # from langchain_ollama import OllamaEmbeddings
# # from langchain_community.chat_models import ChatOllama
# import asyncio
 
# class ChromaClientSingleton:
#     _instance = None

#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super(ChromaClientSingleton, cls).__new__(cls)
#             cls._instance.client = chromadb.PersistentClient()
#         return cls._instance

#     def get_client(self):
#         return self._instance.client


# # Crear instancia única para el cliente Chroma
# # persistent_client = ChromaClientSingleton().get_client()
# persistent_client = chromadb.PersistentClient()
# collection = persistent_client.get_or_create_collection("collection_of_general__information")

# # collection_of_books_ = persistent_client.get_or_create_collection("collection_of_books_",embedding_function= embedding_function)

# collection__of__books = Chroma(
#     client=persistent_client,
#     collection_name="collection__of__books",
#     embedding_function=embedding_function,
#     persist_directory="./chroma-books"  # Especifica el directorio de persistencia
# )

# collection__of__general_information = Chroma(
#     client=persistent_client,
#     collection_name="collection_of_general__information",
#     embedding_function=embedding_function,
#     persist_directory="./chroma-general-information"
# )



# # from langchain_community.document_loaders import PyPDFLoader


# # loader = PyPDFLoader("/Users/alejandroestrada/Documents/Procesos realizados en la Biblioteca Universitaria .pdf")
# # pages = loader.load()

# # text_splitter = RecursiveCharacterTextSplitter(
# #  chunk_size=1500, 
# #  chunk_overlap=150 

# # )

# # splits = text_splitter.split_documents(pages)

# # for split in splits:
# #     split.metadata = DM.metadatas
# # generar mismo id para todos esos fragmentos del mismo documento



# # library_information = Chroma.from_documents(
# #     documents=splits,
# #     embedding=embedding_function,
# #     persist_directory="./filess"
# #     )

import os
import chromadb
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.ollama.ollama_client import OllamaClient
from src.ollama.ollama_embeddings import embedding_function

# Ruta absoluta basada en el archivo actual
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_PATH = os.path.join(BASE_DIR, "chromadb")

class ChromaClientSingleton:
    _instance = None
    _persist_path = None

    def __new__(cls, persist_directory=CHROMA_PATH):
        if cls._instance is None:
            cls._persist_path = persist_directory
            cls._instance = super(ChromaClientSingleton, cls).__new__(cls)
            cls._instance.client = chromadb.PersistentClient(path=persist_directory)
        elif persist_directory != cls._persist_path:
            print(f"Ya existe una instancia con path: {cls._persist_path}, ignorando nuevo path: {persist_directory}")
        return cls._instance

    def get_client(self):
        return self.client

# Crear el cliente con ruta absoluta
chroma_client = ChromaClientSingleton().get_client()

ollama_client = OllamaClient()

# Crear colecciones usando la ruta absoluta
collection__of__books = Chroma(
    client=chroma_client,
    collection_name="collection__of__books",
    embedding_function=ollama_client.embedding_function,
    persist_directory=CHROMA_PATH
)

collection__of__general_information = Chroma(
    client=chroma_client,
    collection_name="collection_of_general__information",
    embedding_function=ollama_client.embedding_function,
    persist_directory=CHROMA_PATH
)

# instance = chromadb.AsyncHttpClient()
# collection__of__thesis = Chroma(
  
#     collection_name="collection_of_thesis",
#     embedding_function=ollama_client.embedding_function,
#     persist_directory='./tesis'
# )

# from langchain_community.document_loaders import PyPDFDirectoryLoader

# loader = PyPDFDirectoryLoader( "/Users/alejandroestrada/Documents/Universidad/Tercer Año/tesis chatbot" ) 
# documents = loader.load()
# print(documents)
# text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=1000,
#             chunk_overlap=100
#         )
        
# splits = text_splitter.split_documents(documents)
# collection__of__thesis.add_documents(
#     documents=splits
# )