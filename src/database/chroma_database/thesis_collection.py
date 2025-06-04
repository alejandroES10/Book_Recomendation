import asyncio
from typing import List, Optional, Tuple
from langchain_core.documents import Document

from src.database.chroma_database.chroma_collection import BaseDocumentCollection
from src.database.chroma_database.vector_store import collection__of__thesis


# class ThesisCollection(ChromaCollection):
#     """Colección para tesis académicas."""

#     def __init__(self):
#         super().__init__()
#         self._collection = collection__of__thesis

#     async def add_documents(self, handle:str,  documents: List[Document]) -> List[str]:
#         try:
#             exist = await self.exists_by_handle(handle)
#             if not exist:
#                 return await self._collection.aadd_documents(documents)
                
#             else:
#                 raise ValueError(f"Ya existe una tesis con el handle: {handle}")
#         except Exception as e:
#             raise ValueError(f"Error al añadir documentos: {e}")
        
#     async def exists_by_handle(self, handle: str) -> bool:
#         try:
#             result = self._collection.get(where={"handle": handle})
#             return bool(result and result['ids'])
#         except Exception as e:
#             raise ValueError(f"Error al verificar existencia de handle '{handle}': {e}");

#     async def delete_documents(self,handle:str) -> List[str]:
        
#             exist = await self.exists_by_handle(handle)
#             if exist:
#                 self._collection._collection.delete(where={"handle": handle})
                
#             else:
#                 raise ValueError(f"No se puede eliminar la tesis porque no existe el handle: {handle}")
            
            
#     async def get_results(self, handle: str) -> dict:
#         return self._collection.get(where={"handle": handle})
    
#     def _format_results(self, result: dict) -> List[dict]:
#         return [
#             {
#                 "id": id_,
#                 "content": doc,
#                 "metadata": meta
#             }
#             for doc, meta, id_ in zip(result["documents"], result["metadatas"], result["ids"])
#         ]

   

#     async def find_one(self, handle: str) -> Optional[dict]:
#         result = await self.get_results(handle)
#         print(result)
#         if not result or not result.get("ids"):
#             raise ValueError(f"No existe información vectorizada del documento con file_id: {file_id}")
#         return self._format_results(result)

#     async def find_all(self) -> List[dict]:
#         result = self._collection.get()
#         return self._format_results(result)

class ThesisCollection(BaseDocumentCollection):
    """Colección para tesis académicas."""

    def __init__(self):
        super().__init__(collection__of__thesis)

    def _build_filter(self, identifier: str) -> dict:
        return {"handle": identifier}


# ************************ Test ***************************************

async def main():
    thesis_collection = ThesisCollection()
    # existing = await thesis_collection.exists_by_handle("123/123")
    # print(f"¿Existe el handle '123/123'? {existing}")
    # await thesis_collection.delete_documents(" ")
    # result = await thesis_collection.find_one("123456789/10201")
    # result = await thesis_collection.find_all()
    result = await thesis_collection.count_distinct_identifiers()
    print(result)

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