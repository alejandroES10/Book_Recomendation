from langchain_ollama import OllamaEmbeddings, ChatOllama

class OllamaClient:
    _instance = None

    def __new__(cls, embedding_model: str = "nomic-embed-text", llm_model: str = "llama3.1", temperature: float = 0.0):
        if cls._instance is None:
            cls._instance = super(OllamaClient, cls).__new__(cls)
            cls._instance.embedding_function = OllamaEmbeddings(model=embedding_model, temperature=temperature)
            cls._instance.llm = ChatOllama(model=llm_model, temperature=temperature)
        return cls._instance
