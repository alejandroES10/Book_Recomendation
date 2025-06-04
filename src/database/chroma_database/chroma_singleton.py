import os
import chromadb
from dotenv import load_dotenv
load_dotenv()
from chromadb.config import Settings


CHROMA_SERVER_HOST: str = os.environ["CHROMA_SERVER_HOST"]
CHROMA_SERVER_PORT: int = int(os.environ["CHROMA_SERVER_PORT"])

class ChromaClient:
    def __init__(self, host: str = CHROMA_SERVER_HOST, port: int = CHROMA_SERVER_PORT):
        """
        Inicializa un nuevo cliente ChromaDB HTTP.
        
        Args:
            host (str): Host del servidor ChromaDB
            port (int): Puerto del servidor ChromaDB
        """
        self._client = chromadb.HttpClient(
            host=host,
            port=port,
            settings=Settings(anonymized_telemetry=False)
        )
    
    def get_client(self):
        """
        Obtiene el cliente ChromaDB configurado.
        
        Returns:
            HttpClient: Instancia del cliente ChromaDB
        """
        return self._client