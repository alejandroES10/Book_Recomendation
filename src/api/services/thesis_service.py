
from typing import List
from src.api.models.document_model import DocumentModel
from src.database.chromadb.thesis_collection import ThesisCollection
from src.api.interfaces.ithesis_service import IThesisService


class ThesisService(IThesisService):
    def __init__(self):
        self.collection = ThesisCollection()
    
    async def add_theses(self, models: List[DocumentModel]) -> List[str]:
        return await self.collection.add_documents(models)

    async def get_thesis(self, id: str) -> dict:
        return await self.collection.find_one(id)

    async def delete_thesis(self, id: str) -> None:
        return await self.collection.delete_documents(id)
