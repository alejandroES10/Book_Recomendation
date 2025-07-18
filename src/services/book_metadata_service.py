import json
from typing import List, Tuple
from src.schemas.book_metadata_schema import BookCreateSchema
from src.database.chroma_database.book_metadata_collection import BookMetadataCollection
from src.interfaces.ibook_metadata_service import IBookMetadataService
from langchain_core.documents import Document
import json
class BookMetadataService(IBookMetadataService):
    def __init__(self):
        self.collection = BookMetadataCollection()
    
    async def add_books(self, books: List[BookCreateSchema]) -> List[str]:
        documents, ids = self._build_chroma_documents(books)
        return await self.collection.add_documents(documents, ids)

    async def get_book(self, id: str) -> dict:
        return await self.collection.find_one(id)

    async def delete_book(self, id: str) -> None:
        return await self.collection.delete_documents(id)

    async def update_book(self, book: BookCreateSchema) -> None:
        list_of_models = book if isinstance(book, list) else [book]
        
        documents, ids = self._build_chroma_documents(list_of_models)
        print(documents)
        print(ids)
        return await self.collection.update_documents(documents, ids)
    
    
    async def get_all_books(self)-> dict:
        return await self.collection.find_all()
    

    

    def _build_chroma_documents(self, models: List[BookCreateSchema]) -> Tuple[List[Document], List[str]]:
        documents = []
        ids = []
        for model in models:
            metadata_text = json.dumps(model.metadata, ensure_ascii=False)
            print(metadata_text)
            documents.append(Document(
                page_content=metadata_text,
                metadata={"fuente": "biblioteca_universitaria"},
                id=str(model.id)
            ))
            ids.append(str(model.id))
        return documents, ids
