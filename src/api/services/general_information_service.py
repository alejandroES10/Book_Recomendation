from typing import List
from src.api.models.document_model import DocumentModel
from src.database.chromadb.general_information_collection import GeneralInformationCollection
from src.api.interfaces.igeneral_information_service import IGeneralInformationService


class GeneralInformationService(IGeneralInformationService):
    def __init__(self):
        self.collection = GeneralInformationCollection()
    
    async def add_general_info(self, models: List[DocumentModel]) -> List[str]:
        return await self.collection.add_documents(models)

    async def get_general_info(self, id: str) -> dict:
        return await self.collection.find_one(id)

    async def delete_general_info(self, id: str) -> None:
        return await self.collection.delete_documents(id)
