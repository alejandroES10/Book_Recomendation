from ctypes import Array
from typing import Any, Dict, List
from fastapi import HTTPException
from langchain_chroma import Chroma
from langchain_core.documents import Document

class ChromaDBService:
    
    def __init__(self, vectore_store: Chroma):
        self._vectore_store = vectore_store

    # def add_document(self, ids: List[str],documents: List[Document]):
    #     return self._collection.add_documents(documents=documents,ids = ids)
    
    def add_documents(self,documents: List[Document]):
        return self._vectore_store.add_documents(documents=documents)
    
    def add_documents_with_ids(self,documents: List[Document],ids: List[str]):
        
        if len(documents) != len(ids):
            raise HTTPException(status_code=400, detail="IDs and documents count mismatch")
        
        elif len(list(self._vectore_store._collection.get(ids).values())[0]) == len(ids):
            raise HTTPException(status_code=400, detail="There is a book with this ID")
        
        return self._vectore_store.add_documents(documents=documents, ids=ids)
    

    def update_documents(self, ids: List[str],documents: List[Document]):
        if len(documents) != len(ids):
            raise HTTPException(status_code=400, detail="IDs and documents count mismatch")
        return self._vectore_store.update_documents(ids=ids, documents=documents)


    def delete_document_by_file_id(self, id: str):
        return self._vectore_store._collection.delete(where={"file_id": id})
    
    def delete_document_by_id(self,id: str):
        self._vectore_store.delete(ids=[id])

    
    def get_documents_by_id(self, ids: List[str]):
        return self._vectore_store.get_by_ids(ids = ids)
    
    def find_one(self,id: str ):
            return self._vectore_store.get(id)
           
        
    def find_all( self):
            return self._vectore_store.get()
        
        

