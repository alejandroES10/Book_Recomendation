import asyncio
from typing import List, Optional, Tuple
from langchain_core.documents import Document

from src.database.chroma_database.chroma_collection import BaseDocumentCollection
from src.database.chroma_database.vector_store import collection__of__thesis



class ThesisCollection(BaseDocumentCollection):
    """Colección para tesis académicas."""

    def __init__(self):
        super().__init__(collection__of__thesis)

    def _build_filter(self, identifier: str) -> dict:
        return {"handle": identifier}


# ************************ Test ***************************************

# async def main():
#     thesis_collection = ThesisCollection()
#     # existing = await thesis_collection.exists_by_handle("123/123")
#     # print(f"¿Existe el handle '123/123'? {existing}")
#     # await thesis_collection.delete_documents(" ")
#     # result = await thesis_collection.find_one("123456789/10201")
#     # result = await thesis_collection.find_all()
#     result = await thesis_collection.count_distinct_identifiers()
#     print(result)

# if __name__ == "__main__":
#     asyncio.run(main())

# # Función para obtener la colección correspondiente por nombre
# def get_collection(name: str) -> Optional[ChromaCollection]:
#     collections = {
#         'collection_of_books': BookMetadata(),
#         'collection_of_general_information': LibraryGeneralInformation(),
#         'collection_of_thesis': ThesisCollection()
#     }
#     return collections.get(name)