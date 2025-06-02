from typing import List, Optional, Tuple
from langchain_core.documents import Document

from src.database.chroma_database.chroma_collection import ChromaCollection
from src.database.chroma_database.vector_store import collection_of_general_information



class GeneralInformationCollection(ChromaCollection):
    """Colección para documentos de información general."""

    def __init__(self):
        self._collection = collection_of_general_information

    async def add_documents(self,file_id: str, documents: List[Document]) -> List[str]:
        try:
            exist = await self._check_file_id_exists(file_id)

            if not exist:
                return await self._collection.aadd_documents(documents)
            raise ValueError(f"Ya existe información vectorizada del documento con file_id: {file_id}")
        except Exception as e:
            raise ValueError(f"Error al añadir documentos: {e}")


    async def get_results(self, file_id: str) -> dict:
        return self._collection.get(where={"file_id": file_id})

    async def _check_file_id_exists(self, file_id: str) -> bool:
        result = await self.get_results(file_id)
        if not result or not result.get("ids"):
            return False
            # raise ValueError(f"No se encontraron documentos con file_id: {file_id}")
        return True

    def _format_results(self, result: dict) -> List[dict]:
        return [
            {
                "id": id_,
                "content": doc,
                "metadata": meta
            }
            for doc, meta, id_ in zip(result["documents"], result["metadatas"], result["ids"])
        ]

    async def delete_documents(self, file_id: str) -> None:
        exist = await self._check_file_id_exists(file_id)
        if exist:
            self._collection._collection.delete(where={"file_id": file_id})
        else:
            raise ValueError(f"No existe información vectorizada del documento con file_id: {file_id}")
        
        
    async def find_one(self, file_id: str) -> List[dict]:
        result = await self.get_results(file_id)
        print(result)
        if not result or not result.get("ids"):
            raise ValueError(f"No existe información vectorizada del documento con file_id: {file_id}")
        return self._format_results(result)

    async def find_all(self) -> List[dict]:
        result = self._collection.get()
        return self._format_results(result)

    
    async def update_documents(self, documents: List[Document], ids:Optional[List[str]]) -> None:
        pass
