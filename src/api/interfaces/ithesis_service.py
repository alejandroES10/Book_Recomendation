from typing import List
from src.api.models.document_model import DocumentModel

class IThesisService:
    def __init__(self):
        pass
    
    async def add_theses(self, models: List[DocumentModel]) -> List[str]:
        pass

    async def get_thesis(self, id: str) -> dict:
        pass

    async def delete_thesis(self, id: str) -> None:
        pass