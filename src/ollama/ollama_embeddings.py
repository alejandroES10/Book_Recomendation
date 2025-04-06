from langchain_ollama import OllamaEmbeddings


embedding_function = OllamaEmbeddings(model = 'nomic-embed-text',temperature=0)