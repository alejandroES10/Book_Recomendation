from typing import List, Optional, Tuple
from langchain_core.documents import Document
from src.api.models.document_model import DocumentModel
from src.database.chromadb.chroma_collection import ChromaCollection
from src.database.chromadb.vector_store import collection_of_general_information



class GeneralInformationCollection(ChromaCollection):
    """Colección para documentos de información general."""

    def __init__(self):
        super().__init__()
        self._collection = collection_of_general_information

    async def add_documents(self, documents: List[Document]) -> List[str]:
        try:
            return await self._collection._vector_store.aadd_documents(documents)
        except Exception as e:
            raise ValueError(f"Error al añadir documentos: {e}")

    async def delete_documents(self, file_id: str) -> None:
        deleted = self._collection._vector_store._collection.delete(where={"file_id": file_id})
        if not deleted:
            raise ValueError(f"No se encontraron documentos con file_id: {file_id}")

    async def find_one(self, id: str) -> Optional[dict]:
        result = self._collection._vector_store.get(ids=[id])
        if not result or not result.get('documents'):
            return None
        return {
            "id": result["ids"][0],
            "content": result["documents"][0],
            "metadata": result["metadatas"][0] if result.get("metadatas") else {}
        }

    async def find_all(self) -> List[dict]:
        result = self._collection._vector_store.get()
        return [{
            "id": id_,
            "content": doc,
            "metadata": meta
        } for doc, meta, id_ in zip(result["documents"], result["metadatas"], result["ids"])]

    async def update_documents(self, elements: List[DocumentModel]) -> None:
        raise NotImplementedError("No se permite actualización en esta colección")

