from typing import List, Tuple
from src.schemas.book_metadata_schema import BookMetadataSchema
from src.database.chromadb.book_metadata_collection import BookMetadataCollection
from src.interfaces.ibook_metadata_service import IBookMetadataService
from langchain_core.documents import Document

class BookMetadataService(IBookMetadataService):
    def __init__(self):
        self.collection = BookMetadataCollection()
    
    async def add_books(self, models: List[BookMetadataSchema]) -> List[str]:
        documents, ids = self._build_chroma_documents(models)
        return await self.collection.add_documents(documents, ids)

    async def get_book(self, id: str) -> dict:
        return await self.collection.find_one(id)

    async def delete_book(self, id: str) -> None:
        return await self.collection.delete_documents(id)

    async def update_book(self, models: BookMetadataSchema) -> None:
        documents, ids = self._build_chroma_documents(models)
        return await self.collection.update_documents(documents, ids)
    
    
    async def get_all_books(self)-> dict:
        return await self.collection.find_all()
    

    
    #**********************************

    def _build_chroma_documents(self, models: List[BookMetadataSchema]) -> Tuple[List[Document], List[str]]:
        documents = []
        ids = []
        for model in models:
            metadata_text = ". ".join([f"{k.capitalize()}: {v}" for k, v in model.metadata.items()]) + "."
            documents.append(Document(
                page_content=metadata_text,
                metadata={"fuente": "biblioteca_universitaria"},
                id=str(model.id)
            ))
            ids.append(str(model.id))
        return documents, ids

   