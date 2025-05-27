from typing import List, Optional, Tuple
from langchain_core.documents import Document
from src.schemas.book_metadata_schema import DocumentModel
from src.database.chromadb.chroma_collection import ChromaCollection
from src.database.chromadb.vector_store import collection__of__thesis


class ThesisCollection(ChromaCollection):
    """Colección para tesis académicas."""

    def __init__(self):
        super().__init__()
        self._collection = collection__of__thesis

    async def add_documents(self, documents: List[Document]) -> List[str]:
        try:
            return await self._collection.aadd_documents(documents)
        except Exception as e:
            raise ValueError(f"Error al añadir documentos: {e}")

    async def delete_documents(self, id: str) -> None:
        try:
            self._collection.delete(ids=[id])
        except Exception as e:
            raise ValueError(f"Error al eliminar documento: {e}")

    async def update_documents(self, documents: List[Document]) -> None:
        try:
            ids = [doc.id for doc in documents]
            self._collection.update_documents(ids=ids, documents=documents)
        except Exception as e:
            raise ValueError(f"Error al actualizar documentos: {e}")

    async def find_one(self, id: str) -> Optional[dict]:
        result = self._collection.get(ids=[id])
        if not result or not result.get('documents'):
            return None
        return {
            "id": result["ids"][0],
            "content": result["documents"][0],
            "metadata": result["metadatas"][0] if result.get("metadatas") else {}
        }

    async def find_all(self) -> List[dict]:
        result = self._collection.get()
        return [{
            "id": id_,
            "content": doc,
            "metadata": meta
        } for doc, meta, id_ in zip(result["documents"], result["metadatas"], result["ids"])]


# # Función para obtener la colección correspondiente por nombre
# def get_collection(name: str) -> Optional[ChromaCollection]:
#     collections = {
#         'collection_of_books': BookMetadata(),
#         'collection_of_general_information': LibraryGeneralInformation(),
#         'collection_of_thesis': ThesisCollection()
#     }
#     return collections.get(name)