
import os
from langchain_ollama import OllamaEmbeddings, ChatOllama

class OllamaClient:
    def __init__(self, 
                 embedding_model: str = "nomic-embed-text", 
                 llm_model: str = "llama3.1", 
                 temperature: float = 0.3):
        """
        Inicializa un nuevo cliente Ollama con modelos para embeddings y LLM.
        
        Args:
            embedding_model (str): Modelo para embeddings (por defecto "nomic-embed-text")
            llm_model (str): Modelo de lenguaje 
            temperature (float): Creatividad del modelo (0.0 más determinista, 1.0 más creativo)
        """
        base_url = os.environ["OLLAMA_BASE_URL"]
        
        self._embedding_function = OllamaEmbeddings(
            model=embedding_model, 
            temperature=temperature, 
            base_url=base_url
        )

        
        self._llm = ChatOllama(
            model=llm_model, 
            temperature=temperature, 
            base_url=base_url, 
            
        )
    
    def get_embedding_function(self):
        """
        Obtiene la función de embeddings configurada.
        
        Returns:
            OllamaEmbeddings: Instancia del generador de embeddings
        """
        return self._embedding_function

    def get_llm(self):
        """
        Obtiene el modelo de lenguaje configurado.
        
        Returns:
            ChatOllama: Instancia del modelo de lenguaje
        """
        return self._llm