
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional



class ChromaCollection(ABC):
    """Clase abstracta base para todas las colecciones de Chroma."""

    def __init__(self):
        self._collection = None

    @abstractmethod
    async def add_documents(self, elements: List[Any]) -> List[str]:
        pass

    @abstractmethod
    async def delete_documents(self, element_id: str) -> None:
        pass

    @abstractmethod
    async def update_documents(self, elements: List[Any]) -> None:
        pass

    @abstractmethod
    async def find_all(self) -> List[Dict]:
        pass

    @abstractmethod
    async def find_one(self, id: str) -> Optional[Dict]:
        pass


