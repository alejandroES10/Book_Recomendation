import os
import chromadb
from dotenv import load_dotenv
load_dotenv()
from chromadb.config import Settings


CHROMA_SERVER_HOST: str = os.environ["CHROMA_SERVER_HOST"]
CHROMA_SERVER_PORT: int = int(os.environ["CHROMA_SERVER_PORT"])
# CHROMA_SERVER_AUTHN_CREDENTIALS: str = os.environ["CHROMA_SERVER_AUTHN_CREDENTIALS"]
# CHROMA_CLIENT_AUTHN_PROVIDER = 'chromadb.auth.token_authn.TokenAuthClientProvider'

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
            settings=Settings(anonymized_telemetry=False,
                            chroma_client_auth_provider=os.getenv("CHROMA_CLIENT_AUTH_PROVIDER"),
                            chroma_client_auth_credentials=os.getenv("CHROMA_CLIENT_AUTH_CREDENTIALS")
            )
                            
        )
    
    def get_client(self):
        """
        Obtiene el cliente ChromaDB configurado.
        
        Returns:
            HttpClient: Instancia del cliente ChromaDB
        """
        return self._client