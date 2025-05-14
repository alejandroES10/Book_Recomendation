import os
import chromadb
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