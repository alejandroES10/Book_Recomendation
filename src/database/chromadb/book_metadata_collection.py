from typing import List, Optional
from langchain_core.documents import Document
from src.database.chromadb.chroma_collection import ChromaCollection
from src.database.chromadb.vector_store import collection_of_books


class BookMetadataCollection(ChromaCollection):
    """Colección especializada en libros con metadatos."""

    def __init__(self):
        self._collection = collection_of_books

    async def _validate_ids_exist(self, ids: List[str]) -> None:
        result = self._collection._vector_store._collection.get(ids=ids)
        if not result or not result.get("ids"):
            raise ValueError("IDs no encontrados en la base de datos")
        missing = [i for i in ids if i not in result["ids"]]
        if missing:
            raise ValueError(f"IDs faltantes en la base de datos: {', '.join(missing)}")

    async def add_documents(self, documents: List[Document], ids: List[str]) -> List[str]:

        existing = self._collection._vector_store._collection.get(ids=ids)
        if existing and existing.get("ids"):
            raise ValueError("IDs duplicados encontrados en la base de datos")
        try:
            return await self._collection._vector_store.aadd_documents(documents=documents, ids=ids)
        except Exception as e:
            raise ValueError(f"Error al añadir documentos: {e}")

    async def update_documents(self, documents: List[Document], ids: List[str]) -> None:
        if len(documents) != len(ids):
            raise ValueError("Cantidad de documentos y de IDs no coinciden")
        await self._validate_ids_exist(ids)
        try:
            await self._collection._vector_store.update_documents(ids=ids, documents=documents)
        except Exception as e:
            raise ValueError(f"Error al actualizar documentos: {e}")

    async def delete_documents(self, id: str) -> None:
        await self._validate_ids_exist([id])
        try:
            self._collection._vector_store.delete(ids=[id])
        except Exception as e:
            raise ValueError(f"Error al eliminar el documento: {e}")

    async def find_one(self, id: str) -> Optional[dict]:
        result = self._collection._vector_store.get(ids=[id])
        if not result or not result.get('documents'):
            return None
        return {
            "id": result["ids"][0],
            "metadata": self._extract_metadata_from_text(result["documents"][0])
        }

    async def find_all(self) -> List[dict]:
        
        result = self._collection.get()
        

        return result