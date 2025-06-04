# import os
# from langchain_ollama import OllamaEmbeddings, ChatOllama

# class OllamaClientSingleton:
#     _instance = None

#     def __new__(cls, embedding_model: str = "nomic-embed-text", llm_model: str = "llama3.1", temperature: float = 0.0):
#         if cls._instance is None:
#             cls._instance = super(OllamaClientSingleton, cls).__new__(cls)
#             base_url = os.environ["OLLAMA_BASE_URL"]
#             cls._instance._embedding_function = OllamaEmbeddings(
#                 model=embedding_model, temperature=temperature, base_url=base_url
#             )
#             cls._instance._llm = ChatOllama(
#                 model=llm_model, temperature=temperature, base_url=base_url, cache=True
#             )
#         return cls._instance

#     def get_embedding_function(self):
#         return self._embedding_function

#     def get_llm(self):
#         return self._llm

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
            llm_model (str): Modelo de lenguaje (por defecto "llama3.1")
            temperature (float): Creatividad del modelo (0.0 más determinista, 1.0 más creativo)
        """
        base_url = os.environ["OLLAMA_BASE_URL"]
        
        self._embedding_function = OllamaEmbeddings(
            model=embedding_model, 
            temperature=temperature, 
            base_url=base_url
        )

        # self._llm = ChatOllama(
        #     model="llama3.1",  # Modelo de 70B parámetros
        #     temperature=0.7,     # Balance creatividad/precisión
        #            # Contexto amplio
        #     top_p=0.9
        #     # top_k=40
        #     # repeat_penalty=1.1,
        #     # stop=["\n", "###"],  # Secuencias de parada
        #            # Usar GPU si está disponible
        #      # URL de tu servidor Ollama
        # )
        
        self._llm = ChatOllama(
            model=llm_model, 
            temperature=temperature, 
            base_url=base_url, 
            # cache=True
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