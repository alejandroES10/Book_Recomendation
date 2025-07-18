from typing import List, Optional, Tuple
from langchain_core.documents import Document

from src.database.chroma_database.chroma_collection import BaseDocumentCollection
from src.database.chroma_database.vector_store import collection_of_general_information



class GeneralInformationCollection(BaseDocumentCollection):
    """Colección para documentos de información general."""

    def __init__(self):
        super().__init__(collection_of_general_information)

    def _build_filter(self, identifier: str) -> dict:
        return {"file_id": identifier}