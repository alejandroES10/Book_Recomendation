# import os
# import chromadb
# from langchain_chroma import Chroma
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from src.ollama.ollama_client import OllamaClient
# from src.ollama.ollama_embeddings import embedding_function

# # Ruta absoluta basada en el archivo actual
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# CHROMA_PATH = os.path.join(BASE_DIR, "chromadb")

# class ChromaClientSingleton:
#     _instance = None
#     _persist_path = None

#     def __new__(cls, persist_directory=CHROMA_PATH):
#         if cls._instance is None:
#             cls._persist_path = persist_directory
#             cls._instance = super(ChromaClientSingleton, cls).__new__(cls)
#             cls._instance.client = chromadb.PersistentClient(path=persist_directory)
#         elif persist_directory != cls._persist_path:
#             print(f"Ya existe una instancia con path: {cls._persist_path}, ignorando nuevo path: {persist_directory}")
#         return cls._instance

#     def get_client(self):
#         return self.client

# # Crear el cliente con ruta absoluta
# chroma_client = ChromaClientSingleton().get_client()

# ollama_client = OllamaClient()

# # Crear colecciones usando la ruta absoluta
# collection__of__books = Chroma(
#     client=chroma_client,
#     collection_name="collection__of__books",
#     embedding_function=ollama_client.embedding_function,
#     persist_directory=CHROMA_PATH
# )

# collection__of__general_information = Chroma(
#     client=chroma_client,
#     collection_name="collection_of_general__information",
#     embedding_function=ollama_client.embedding_function,
#     persist_directory=CHROMA_PATH
# )
import os
import uuid
import chromadb
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.ollama.ollama_client import OllamaClientSingleton
# from src.ollama.ollama_embeddings import embedding_function

from dotenv import load_dotenv
load_dotenv()


CHROMA_SERVER_HOST: str = os.environ["CHROMA_SERVER_HOST"]
CHROMA_SERVER_PORT: int = int(os.environ["CHROMA_SERVER_PORT"])

class ChromaClientSingleton:
    _instance = None

    def __new__(cls, host: str = CHROMA_SERVER_HOST, port: int = CHROMA_SERVER_PORT):
        if cls._instance is None:
            cls._instance = super(ChromaClientSingleton, cls).__new__(cls)
            cls._instance._client = chromadb.HttpClient(host=host, port=port)
        return cls._instance

    def get_client(self):
        return self._client

# Crear el cliente conectado al servidor Chroma
chroma_client = ChromaClientSingleton().get_client()

ollama_client = OllamaClientSingleton()

# Crear colecciones SIN persist_directory, ya que el servidor se encarga
collection_of_books = Chroma(
    client=chroma_client,
    collection_name="collection_of_books",
    embedding_function=ollama_client.get_embedding_function(),
)

collection_of_general_information = Chroma(
    client=chroma_client,
    collection_name="collection_of_general_information",
    embedding_function=ollama_client.get_embedding_function(),
)


# instance = chromadb.AsyncHttpClient()
collection__of__thesis = Chroma(
    client=chroma_client,
    collection_name="collection_of_thesis",
    embedding_function=ollama_client.get_embedding_function(),
)

from langchain_community.document_loaders import PyPDFLoader

def addTesis(rute: str, metadata: dict) -> None:
    """
    Carga documentos PDF desde una ruta específica, los divide en fragmentos y los agrega a la colección de tesis.
    """
    # Cargar documentos PDF desde la ruta especificada
    loader = PyPDFLoader(rute)
    documents = loader.load()

    # Dividir los documentos en fragmentos
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    splits = text_splitter.split_documents(documents)

    for split in splits:
        split.metadata.update(metadata)

    # Agregar los fragmentos a la colección de tesis
    collection__of__thesis.add_documents(splits)

# addTesis(
#     rute="/Users/alejandroestrada/Documents/Universidad/Tercer Año/Tesis Descargadas/2014_cepero_perez_nayma.pdf",
#     metadata={
#         "id": 1,
#         "titulo": "Componente de aprendizaje para agentes JADE",
#         "autor": "Nayma Cepero Pérez",
#         "fecha": "2022-11-01",
#         "enlace_url": "https://universidadeuropea.com/blog/agentes-inteligentes/#:~:text=Los%20agentes%20inteligentes%20comparten%20una,su%20comportamiento%20seg%C3%BAn%20sus%20vivencias."
#     }
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