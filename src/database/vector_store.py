from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.ollama.ollama_embeddings import embedding_function
import chromadb
# from langchain_ollama import OllamaEmbeddings
# from langchain_community.chat_models import ChatOllama
import asyncio
 
class ChromaClientSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChromaClientSingleton, cls).__new__(cls)
            cls._instance.client = chromadb.PersistentClient()
        return cls._instance

    def get_client(self):
        return self._instance.client


# Crear instancia única para el cliente Chroma
persistent_client = ChromaClientSingleton().get_client()
# persistent_client = chromadb.PersistentClient()

# collection_of_books_ = persistent_client.get_or_create_collection("collection_of_books_",embedding_function= embedding_function)

collection__of__books = Chroma(
    client=persistent_client,
    collection_name="collection__of__books",
    embedding_function=embedding_function,
    
)

collection__of__general_information = Chroma(
    client=persistent_client,
    collection_name="collection_of_general_information",
    embedding_function=embedding_function,
    persist_directory="./general_info"
)



from langchain_community.document_loaders import PyPDFLoader


loader = PyPDFLoader("/Users/alejandroestrada/Documents/Procesos realizados en la Biblioteca Universitaria .pdf")
pages = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
 chunk_size=1500, 
 chunk_overlap=150 

)

splits = text_splitter.split_documents(pages)

# for split in splits:
#     split.metadata = DM.metadatas
# generar mismo id para todos esos fragmentos del mismo documento



library_information = Chroma.from_documents(
    documents=splits,
    embedding=embedding_function,
    persist_directory="./filess"
    )

