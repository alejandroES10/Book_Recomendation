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

    async def delete_documents(self, vectorization_id: str) -> None:
        exist = self._collection.get(where={"vectorization_id": vectorization_id})
        if not exist or not exist.get('ids'):
            raise ValueError(f"No se encontraron documentos con vectorization_id: {vectorization_id}")
        
        self._collection._collection.delete(where={"vectorization_id": vectorization_id})
    
        # if not deleted:
        #     raise ValueError(f"No se encontraron documentos con vectorization_id: {vectorization_id}")

    async def find_one(self, vectorization_id: str) -> List[dict]:
        result = self._collection._collection.get(where={"vectorization_id": vectorization_id})
        print(result)
        if not result or len(result.get('ids')) == 0:
            print("*******************")
            raise ValueError(f"No se encontraron documentos con vectorization_id: {vectorization_id}")

        return [{
            "id": id_,
            "content": doc,
            "metadata": meta
        } for doc, meta, id_ in zip(result["documents"], result["metadatas"], result["ids"])]

    async def find_all(self) -> List[dict]:
        result = self._collection.get()
        return [{
            "id": id_,
            "content": doc,
            "metadata": meta
        } for doc, meta, id_ in zip(result["documents"], result["metadatas"], result["ids"])]

    # async def update_documents(self, elements: List[DocumentModel]) -> None:
    #     raise NotImplementedError("No se permite actualización en esta colección")

    async def update_documents(self, documents: List[Document], ids:Optional[List[str]]) -> None:
        pass
