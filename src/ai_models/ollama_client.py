import os
from langchain_ollama import OllamaEmbeddings, ChatOllama

class OllamaClientSingleton:
    _instance = None

    def __new__(cls, embedding_model: str = "nomic-embed-text", llm_model: str = "llama3.1", temperature: float = 0.0):
        if cls._instance is None:
            cls._instance = super(OllamaClientSingleton, cls).__new__(cls)
            base_url = os.environ["OLLAMA_BASE_URL"]
            cls._instance._embedding_function = OllamaEmbeddings(
                model=embedding_model, temperature=temperature, base_url=base_url
            )
            cls._instance._llm = ChatOllama(
                model=llm_model, temperature=temperature, base_url=base_url, cache=True
            )
        return cls._instance

    def get_embedding_function(self):
        return self._embedding_function

    def get_llm(self):
        return self._llm
