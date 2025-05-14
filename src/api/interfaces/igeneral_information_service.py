from typing import List

from fastapi import File
from src.api.models.document_model import DocumentModel

class IGeneralInformationService:

    def __init__(self):
        pass
    
    async def add_general_info(self, file: File) -> List[str]:
        pass

    async def get_general_info(self, id: str) -> dict:
        pass

    async def get_all_general_info(self) -> dict:
        pass

    async def delete_general_info(self, id: str) -> None:
        pass