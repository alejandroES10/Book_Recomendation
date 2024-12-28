from typing import Any, Dict, List
from langchain_chroma import Chroma
from langchain_core.documents import Document

class ChromaDBService:
    
    def __init__(self, collection: Chroma):
        self._collection = collection

    # def add_document(self, ids: List[str],documents: List[Document]):
    #     return self._collection.add_documents(documents=documents,ids = ids)
    
    def add_document(self,documents: List[Document]):
        return self._collection.add_documents(documents=documents)
    

    def update_document(self, ids: List[str],documents: List[Document]):
        return self._collection.update_documents(ids=ids, documents=documents)


    def delete_document(self, id: str):
        return self._collection.delete(where={"file_id": id})
    

    def get_documents_by_id(self, ids: List[str]):
        return self._collection.get_by_ids(ids = ids)
        
    def find_all( self):
            return self._collection.get()
        
        
    def _generate_id(self) -> str:
        import uuid
        return str(uuid.uuid4())
