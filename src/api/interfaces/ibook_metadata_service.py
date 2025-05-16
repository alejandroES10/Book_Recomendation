


from abc import ABC, abstractmethod
from typing import List
from src.api.models.book_metadata_model import BookMetadataModel


class IBookMetadataService(ABC):

    @abstractmethod
    async def add_books(self, models: List[BookMetadataModel]) -> List[str]:
        pass

    @abstractmethod
    async def get_book(self, id: str) -> dict:
        pass

    @abstractmethod
    async def delete_book(self, id: str) -> None:
        pass

    @abstractmethod
    async def update_book(self, id: str, model: BookMetadataModel) -> None:
        pass


    @abstractmethod
    async def get_all_books(self)-> dict:
        pass