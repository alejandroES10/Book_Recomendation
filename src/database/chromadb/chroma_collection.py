
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from langchain_core.documents import Document



class ChromaCollection(ABC):
    """Clase abstracta base para todas las colecciones de Chroma."""

    def __init__(self):
        self._collection = None

    @abstractmethod
    async def add_documents(self, documents: List[Document], ids:Optional[List[str]]) -> List[str]:
        pass


    @abstractmethod
    async def delete_documents(self, document_id: str) -> None:
        pass

    @abstractmethod
    async def update_documents(self, documents: List[Document], ids:Optional[List[str]]) -> None:
        pass

    @abstractmethod
    async def find_all(self) -> List[Dict]:
        pass

    @abstractmethod
    async def find_one(self, document_id: str) -> Optional[Dict]:
        pass


