from typing import List, Optional, Tuple
from langchain_core.documents import Document

from src.database.chromadb.chroma_collection import ChromaCollection
from src.database.chromadb.vector_store import collection_of_general_information



class GeneralInformationCollection(ChromaCollection):
    """Colección para documentos de información general."""

    def __init__(self):
        self._collection = collection_of_general_information

    async def add_documents(self, documents: List[Document]) -> List[str]:
        try:
            return await self._collection.aadd_documents(documents)
        except Exception as e:
            raise ValueError(f"Error al añadir documentos: {e}")

    def _check_vectorization_exists(self, vectorization_id: str) -> dict:
        result = self._collection.get(where={"vectorization_id": vectorization_id})
        if not result or not result.get("ids"):
            raise ValueError(f"No se encontraron documentos con vectorization_id: {vectorization_id}")
        return result

    def _format_results(self, result: dict) -> List[dict]:
        return [
            {
                "id": id_,
                "content": doc,
                "metadata": meta
            }
            for doc, meta, id_ in zip(result["documents"], result["metadatas"], result["ids"])
        ]

    async def delete_documents(self, vectorization_id: str) -> None:
        self._check_vectorization_exists(vectorization_id)
        self._collection._collection.delete(where={"vectorization_id": vectorization_id})

    async def find_one(self, vectorization_id: str) -> List[dict]:
        result = self._check_vectorization_exists(vectorization_id)
        return self._format_results(result)

    async def find_all(self) -> List[dict]:
        result = self._collection.get()
        return self._format_results(result)

    
    async def update_documents(self, documents: List[Document], ids:Optional[List[str]]) -> None:
        pass
