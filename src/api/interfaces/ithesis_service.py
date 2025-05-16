from abc import abstractmethod
from typing import List
from src.api.models.book_metadata_model import DocumentModel

class IThesisService:
    
    @abstractmethod
    async def add_theses(self, models: List[DocumentModel]) -> List[str]:
        pass

    @abstractmethod
    async def get_thesis(self, id: str) -> dict:
        pass
    
    @abstractmethod
    async def delete_thesis(self, id: str) -> None:
        pass