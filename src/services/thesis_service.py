
from typing import List
from src.schemas.book_metadata_schema import DocumentModel
from src.database.chroma_database.thesis_collection import ThesisCollection
from src.interfaces.ithesis_service import IThesisService


class ThesisService(IThesisService):
    def __init__(self):
        self.collection = ThesisCollection()
    
    async def add_theses(self, models: List[DocumentModel]) -> List[str]:
        return await self.collection.add_documents(models)

    async def get_thesis(self, id: str) -> dict:
        return await self.collection.find_one(id)

    async def delete_thesis(self, id: str) -> None:
        return await self.collection.delete_documents(id)
