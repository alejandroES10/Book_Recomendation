from typing import List, Optional, Tuple
from langchain_chroma import Chroma
from langchain_core.documents import Document
from src.api.models.book_metadata_model import BookMetadataModel 

class ChromaDBService:
    def __init__(self, vector_store: Chroma):
        self._vector_store = vector_store

    async def add_documents(self, documents: List[Document]) -> List[str]:
        try:
            return await self._vector_store.aadd_documents(documents)
        except Exception as e:
            raise ValueError(f"Failed to add documents: {str(e)}")

    async def add_documents_with_ids(self, models: List[BookMetadataModel]) -> None:
        documents, ids = self._build_chroma_documents(models)

        existing = self._vector_store._collection.get(ids=ids)
        if existing and len(existing['ids']) > 0:
            raise ValueError("Duplicate ID found in the database")
        
        try:
            await self._vector_store.aadd_documents(documents=documents, ids=ids)
        except Exception as e:
            raise ValueError(f"Failed to add documents: {str(e)}")

    # async def update_documents(self, models: List[DocumentModel]) -> None:
    #     documents, ids = self._build_chroma_documents(models)

    #     try:
    #         self._vector_store.update_documents(ids=ids, documents=documents)
    #     except Exception as e:
    #         raise ValueError(f"Failed to update documents: {str(e)}")

    async def update_documents(self, models: List[BookMetadataModel]) -> None:
        documents, ids = self._build_chroma_documents(models)

        if len(documents) != len(ids):
            raise ValueError("IDs and documents count mismatch")

        await self._validate_ids_exist(ids)

        try:
            self._vector_store.update_documents(ids=ids, documents=documents)
        except Exception as e:
            raise ValueError(f"Failed to update documents: {str(e)}")


    async def delete_document_by_file_id(self, file_id: str) -> None:
        result = self._vector_store._collection.delete(where={"file_id": file_id})
        if not result:
            raise ValueError(f"No documents found with file_id: {file_id}")
        
    async def delete_document_by_id(self, id: str) -> None:
        await self._validate_ids_exist([id])
        try:
            self._vector_store.delete(ids=[id])
        except Exception as e:
            raise ValueError(f"Failed to delete document: {str(e)}")


    # async def delete_document_by_id(self, id: str) -> None:
    #     try:
    #         self._vector_store.delete(ids=[id])
    #     except Exception as e:
    #         raise ValueError(f"Failed to delete document: {str(e)}")

    # async def find_one(self, id: str) -> Optional[Document]:
    #     result = self._vector_store.get(ids=[id])
    #     if not result or not result['documents']:
    #         return None
    #     return Document(
    #         page_content=result['documents'][0],
    #         metadata=result['metadatas'][0],
    #         id=result['ids'][0]
    #     )

    # async def find_all(self) -> List[Document]:
    #     result = self._vector_store.get()
    #     return [
    #         Document(
    #             page_content=doc,
    #             metadata=meta,
    #             id=id_
    #         ) for doc, meta, id_ in zip(
    #             result['documents'],
    #             result['metadatas'],
    #             result['ids']
    #         )
    #     ]
    async def find_one(self, id: str) -> Optional[dict]:
        result = self._vector_store.get(ids=[id])
        if not result or not result['documents']:
            return None
        
        page_content = result['documents'][0]
        metadata = self._extract_metadata_from_text(page_content)

        return {
            "id": result['ids'][0],
            "metadata": metadata
        }
    
    async def find_all(self) -> List[dict]:
        result = self._vector_store.get()
        return [
            {
                "id": id_,
                "metadata": self._extract_metadata_from_text(doc)
            } for doc, id_ in zip(result['documents'], result['ids'])
        ]



    def _build_chroma_documents(self, models: List[BookMetadataModel]) -> Tuple[List[Document], List[str]]:
        """Transforma modelos de entrada en objetos Document de LangChain"""
        documents = []
        ids = []

        for model in models:
            metadata_text = ". ".join(
                [f"{key.capitalize()}: {value}" for key, value in model.metadata.items()]
            ) + "."

            doc = Document(
                page_content=metadata_text,
                metadata={"fuente": "biblioteca_universitaria"},
                id=str(model.id)
            )
            documents.append(doc)
            ids.append(str(model.id))

        return documents, ids
    
    def _extract_metadata_from_text(self, text: str) -> dict:
        """
        Convierte el texto del page_content de vuelta a un diccionario de metadatos.
        Ejemplo de entrada:
        "Título: Redes neuronales. Autor: Juan Pérez. Año: 2022."
        """
        metadata = {}
        pairs = text.strip().split(". ")
        for pair in pairs:
            if ": " in pair:
                key, value = pair.split(": ", 1)
                metadata[key.lower()] = value.strip(".")
        return metadata

    async def _validate_ids_exist(self, ids: List[str]) -> None:
        """Verifica que todos los IDs existan en la colección"""
        existing = self._vector_store._collection.get(ids=ids)
        if not existing or not existing.get("ids"):
            raise ValueError("None of the provided IDs exist in the database")

        existing_ids_set = set(existing["ids"])
        missing_ids = [doc_id for doc_id in ids if doc_id not in existing_ids_set]

        if missing_ids:
            raise ValueError(f"The following IDs do not exist in the database: {', '.join(missing_ids)}")



# from typing import List, Optional
# from fastapi import HTTPException
# from langchain_chroma import Chroma
# from langchain_core.documents import Document

# class ChromaDBService:
#     def __init__(self, vector_store: Chroma):
#         self._vector_store = vector_store

#     async def add_documents(self, documents: List[Document]) -> List[str]:
#         """Add documents to the vector store without specific IDs"""
#         try:
#             return await self._vector_store.aadd_documents(documents)
#         except Exception as e:
#             raise ValueError(f"Failed to add documents: {str(e)}")

#     async def add_documents_with_ids(self, documents: List[Document], ids: List[str]) -> None:
#         """Add documents with specific IDs"""
#         if len(documents) != len(ids):
#             raise ValueError("IDs and documents count mismatch")
        
#         existing = self._vector_store._collection.get(ids=ids)
#         if existing and len(existing['ids']) > 0:
#             raise ValueError("Duplicate ID found in the database")
        
#         try:
#             await self._vector_store.aadd_documents(documents=documents, ids=ids)
#         except Exception as e:
#             raise ValueError(f"Failed to add documents: {str(e)}")

#     async def update_documents(self, ids: List[str], documents: List[Document]) -> None:
#         """Update existing documents"""
#         if len(documents) != len(ids):
#             raise ValueError("IDs and documents count mismatch")
        
#         try:
#             await self._vector_store.aupdate_documents(ids=ids, documents=documents)
#         except Exception as e:
#             raise ValueError(f"Failed to update documents: {str(e)}")

#     async def delete_document_by_file_id(self, file_id: str) -> None:
#         """Delete documents by file_id metadata"""
#         result = self._vector_store._collection.delete(where={"file_id": file_id})
#         if not result:
#             raise ValueError(f"No documents found with file_id: {file_id}")

#     async def delete_document_by_id(self, id: str) -> None:
#         """Delete document by ID"""
#         try:
#             self._vector_store.delete(ids=[id])
#         except Exception as e:
#             raise ValueError(f"Failed to delete document: {str(e)}")

#     async def find_one(self, id: str) -> Optional[Document]:
#         """Find a single document by ID"""
#         result = self._vector_store.get(ids=[id])
#         if not result or not result['documents']:
#             return None
#         return Document(
#             page_content=result['documents'][0],
#             metadata=result['metadatas'][0],
#             id=result['ids'][0]
#         )

#     async def find_all(self) -> List[Document]:
#         """Get all documents from the collection"""
#         result = self._vector_store.get()
#         return [
#             Document(
#                 page_content=doc,
#                 metadata=meta,
#                 id=id_
#             ) for doc, meta, id_ in zip(
#                 result['documents'],
#                 result['metadatas'],
#                 result['ids']
#             )
#         ]


# from ctypes import Array
# from typing import Any, Dict, List
# from fastapi import HTTPException
# from langchain_chroma import Chroma
# from langchain_core.documents import Document

# class ChromaDBService:
    
#     def __init__(self, vectore_store: Chroma):
#         self._vectore_store = vectore_store

#     # def add_document(self, ids: List[str],documents: List[Document]):
#     #     return self._collection.add_documents(documents=documents,ids = ids)
    
#     def add_documents(self,documents: List[Document]):
#         return self._vectore_store.add_documents(documents=documents)
    
#     def add_documents_with_ids(self,documents: List[Document],ids: List[str]):
        
#         if len(documents) != len(ids):
#             raise HTTPException(status_code=400, detail="IDs and documents count mismatch")
        
#         elif len(list(self._vectore_store._collection.get(ids).values())[0]) == len(ids):
#             raise HTTPException(status_code=400, detail="There is a book with this ID")
        
#         return self._vectore_store.add_documents(documents=documents, ids=ids)
    

#     def update_documents(self, ids: List[str],documents: List[Document]):
#         if len(documents) != len(ids):
#             raise HTTPException(status_code=400, detail="IDs and documents count mismatch")
#         return self._vectore_store.update_documents(ids=ids, documents=documents)


#     def delete_document_by_file_id(self, id: str):
#         return self._vectore_store._collection.delete(where={"file_id": id})
    
#     def delete_document_by_id(self,id: str):
#         self._vectore_store.delete(ids=[id])

    
#     def get_documents_by_id(self, ids: List[str]):
#         return self._vectore_store.get_by_ids(ids = ids)
    
#     def find_one(self,id: str ):
#             return self._vectore_store.get(id)
           
        
#     def find_all( self):
#             return self._vectore_store.get()
        
        

