
import os
import uuid
import chromadb
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.ai_models.ollama_client import OllamaClient
from src.database.chroma_database.chroma_singleton import ChromaClient
# from src.ollama.ollama_embeddings import embedding_function



# Crear el cliente conectado al servidor Chroma
chroma_client = ChromaClient().get_client()

ollama_client = OllamaClient()

# Crear colecciones SIN persist_directory, ya que el servidor se encarga
collection_of_books = Chroma(
    client= chroma_client,
    collection_name="collection_of_books",
    embedding_function=ollama_client.get_embedding_function(),
)
# async def c():
#     client = await chromadb.AsyncHttpClient(host=os.environ["CHROMA_SERVER_HOST"], port=int(os.environ["CHROMA_SERVER_PORT"]), settings=chromadb.config.Settings(anonymized_telemetry=False))
#     print("Conectando al cliente Chroma...")
#     print(client)
#     collection_of_books = Chroma(
#         client= client,
#         collection_name="collection_of_aceite",
#         embedding_function=ollama_client.get_embedding_function(),
#     )
#     return collection_of_books

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