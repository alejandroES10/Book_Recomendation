import asyncio
from typing import List, Optional, Tuple
from langchain_core.documents import Document

from src.database.chroma_database.chroma_collection import ChromaCollection
from src.database.chroma_database.vector_store import collection__of__thesis


class ThesisCollection(ChromaCollection):
    """Colección para tesis académicas."""

    def __init__(self):
        super().__init__()
        self._collection = collection__of__thesis

    async def add_documents(self,handle:str,  documents: List[Document]) -> List[str]:
        try:
            exist = await self.exists_by_handle(handle)
            if exist:
                raise ValueError(f"Ya existe una tesis con el handle: {handle}")
            return await self._collection.aadd_documents(documents)
        except Exception as e:
            raise ValueError(f"Error al añadir documentos: {e}")
        
    async def exists_by_handle(self, handle: str) -> bool:
        try:
            result = self._collection.get(where={"handle": handle})
            return bool(result and result['ids'])
        except Exception as e:
            raise ValueError(f"Error al verificar existencia de handle '{handle}': {e}");

    async def delete_documents_by_handle(self,handle:str) -> List[str]:
        try:
            exist = await self.exists_by_handle(handle)
            if not exist:
                raise ValueError(f"No se puede eliminar la tesis porque no existe el handle: {handle}")
            print("Existe el handle")
            self._collection._collection.delete(where={"handle": handle})

        except Exception as e:
            raise ValueError(f"Error al añadir documentos: {e}")



    async def delete_documents(self, id: str) -> None:
        pass

    async def update_documents(self, documents: List[Document]) -> None:
        pass

    async def find_one(self, id: str) -> Optional[dict]:
        pass

    async def find_all(self) -> List[dict]:
        pass

# ************************ Test ***************************************

async def main():
    thesis_collection = ThesisCollection()
    # existing = await thesis_collection.exists_by_handle("123/123")
    # print(f"¿Existe el handle '123/123'? {existing}")
    await thesis_collection.delete_documents_by_handle("123456789/10201")

if __name__ == "__main__":
    asyncio.run(main())

# # Función para obtener la colección correspondiente por nombre
# def get_collection(name: str) -> Optional[ChromaCollection]:
#     collections = {
#         'collection_of_books': BookMetadata(),
#         'collection_of_general_information': LibraryGeneralInformation(),
#         'collection_of_thesis': ThesisCollection()
#     }
#     return collections.get(name)