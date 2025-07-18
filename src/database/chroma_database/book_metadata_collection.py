import json
from typing import List, Optional
from langchain_core.documents import Document
from src.database.chroma_database.chroma_collection import BaseCollection
from src.database.chroma_database.vector_store import collection_of_books


class BookMetadataCollection(BaseCollection):
    """Colección especializada en libros con metadatos."""

    def __init__(self):
        super().__init__(collection_of_books)

    def _validate_ids(self, ids: List[str]):
        if not ids or not all(i.strip() for i in ids):
            raise ValueError("La lista de IDs no puede estar vacía ni contener elementos vacíos")

    async def _validate_ids_exist(self, ids: List[str]) -> None:
        self._validate_ids(ids)
        result = self._collection._collection.get(ids=ids)
        if not result or not result.get("ids"):
            raise ValueError("ID no encontrado")
        missing = [i for i in ids if i not in result["ids"]]
        if missing:
            raise ValueError(f"IDs faltantes en la base de datos: {', '.join(missing)}")

    async def add_documents(self, documents: List[Document], ids: List[str]) -> List[str]:
        self._validate_ids(ids)
        self._validate_documents(documents)
        existing = self._collection._collection.get(ids=ids)
        if existing and existing.get("ids"):
            existing_ids = existing["ids"]
            error_detail = {
                "message": "No se pudieron agregar los documentos porque ya existen los siguientes IDs",
                "existing_ids": existing_ids
            }
            raise ValueError(error_detail)
        try:
            return await self._collection.aadd_documents(documents=documents, ids=ids)
        except Exception as e:
            raise ValueError(f"Error al añadir documentos: {e}")

    async def update_documents(self, documents: List[Document], ids: List[str]) -> None:
        self._validate_ids(ids)
        self._validate_documents(documents)
        if len(documents) != len(ids):
            raise ValueError("Cantidad de documentos y de IDs no coinciden")
        await self._validate_ids_exist(ids)
        try:
            self._collection.update_documents(ids=ids, documents=documents)
        except Exception as e:
            raise ValueError(f"Error al actualizar documentos: {e}")

    async def delete_documents(self, id: str) -> None:
        self._validate_identifier(id)
        await self._validate_ids_exist([id])
        try:
            self._collection.delete(ids=[id])
        except Exception as e:
            raise ValueError(f"Error al eliminar el documento: {e}")

    async def find_one(self, id: str) -> Optional[dict]:
        self._validate_identifier(id)
        result = self._collection.get(ids=[id])

        if not result or not result.get("ids"):
            raise ValueError("No hay libro con ese ID")
        return {
            "id": result["ids"][0],
            "metadata": self._extract_metadata_from_text(result["documents"][0])
        }

    async def find_all(self) -> List[dict]:
        
        result = self._collection.get()
    
        return [
            {
                "id": id_,
                "metadata": self._extract_metadata_from_text(doc)
            } for doc, id_ in zip(result['documents'], result['ids'])
        ]
    
    # def _extract_metadata_from_text(self, text: str) -> dict:
    #     metadata = {}
    #     # for item in text.strip().split(". "):
    #     #     if ": " in item:
    #     #         key, value = item.split(": ", 1)
    #     #         metadata[key.lower()] = value.strip(".")
    #     for item in text.strip().split("|||"):
    #         print(item)
    #         if "::" in item:
    #             key, value = item.split("::", 1)
    #             metadata[key] = value.strip()
    #     return metadata
    def _extract_metadata_from_text(self, text: str) -> dict:
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            raise ValueError("El contenido del documento no es un JSON válido")