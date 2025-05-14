from typing import List
from src.api.models.document_model import BookMetadataModel
from src.database.chromadb.book_metadata_collection import BookMetadataCollection
from src.api.interfaces.ibook_metadata_service import IBookMetadataService

class BookService(IBookMetadataService):
    def __init__(self):
        self.collection = BookMetadataCollection()
    
    async def add_books(self, models: List[BookMetadataModel]) -> List[str]:
        return await self.collection.add_documents(models)

    async def get_book(self, id: str) -> dict:
        return await self.collection.find_one(id)

    async def delete_book(self, id: str) -> None:
        return await self.collection.delete_documents(id)

    async def update_book(self, id: str, model: BookMetadataModel) -> None:
        return await self.collection.update_document(id, model)