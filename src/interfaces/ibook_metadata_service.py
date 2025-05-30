


from abc import ABC, abstractmethod
from typing import List
from src.schemas.book_metadata_schema import BookMetadataSchema


class IBookMetadataService(ABC):

    @abstractmethod
    async def add_books(self, models: List[BookMetadataSchema]) -> List[str]:
        pass

    @abstractmethod
    async def get_book(self, id: str) -> dict:
        pass

    @abstractmethod
    async def delete_book(self, id: str) -> None:
        pass

    @abstractmethod
    async def update_book(self, models: BookMetadataSchema) -> None:
        pass    


    @abstractmethod
    async def get_all_books(self)-> dict:
        pass