from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from ollama.ollama_embeddings import embedding_function
# import chromadb
# from langchain_ollama import OllamaEmbeddings
# from langchain_community.chat_models import ChatOllama
import asyncio
 
# persistent_client = chromadb.PersistentClient()

# collection_of_books = persistent_client.get_or_create_collection("collection_of_books")

documents = [
    Document(
        page_content="Los perros son excelentes compañeros, conocidos por su lealtad y amabilidad.",
        metadata={"source": "documento-mamiferos-mascotas"},
        
    ),
    Document(
        page_content="Los gatos son mascotas independientes que a menudo disfrutan de su propio espacio.",
        metadata={"source": "documento-mamiferos-mascotas"},
    ),
    Document(
        page_content="Los peces dorados son mascotas populares para principiantes, ya que requieren un cuidado relativamente simple.",
        metadata={"source": "documento-peces-mascotas"},
    ),
    Document(
        page_content="Los loros son aves inteligentes capaces de imitar el habla humana.",
        metadata={"source": "documento-aves-mascotas"},
    ),
    Document(
        page_content="Los conejos son animales sociales que necesitan mucho espacio para saltar.",
        metadata={"source": "documento-mamiferos-mascotas"},
    ),
]

# collection_of_books.add(documents= documents, ids=["1","2","3","4","5"])


# vectorstore_of_books = Chroma(
#     client=persistent_client,
#     collection_name= "collection_of_books",
#     embedding_function=embedding_function,
# )

vectorstore_of_books = Chroma.from_documents(
    documents= documents,
    # ids=["1","2","3","4","5"],
    embedding= embedding_function
)

