


from abc import ABC
from typing import List
from src.api.models.document_model import BookMetadataModel


class IBookMetadataService(ABC):

    def __init__(self):
        pass
  
    async def add_books(self, models: List[BookMetadataModel]) -> List[str]:
        pass

    async def get_book(self, id: str) -> dict:
        pass

    async def delete_book(self, id: str) -> None:
        pass

    async def update_book(self, id: str, model: BookMetadataModel) -> None:
        pass


    async def get_all_books(self)-> dict:
        pass