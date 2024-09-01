from database.vector_store import  collection__of__books
# from database.vector_store import vectorstore_of_thesis
from langchain_core.documents import Document
from fastapi import HTTPException
from typing import List
from api.models.document_model import DocumentModel
from uuid import uuid4


class DocumentService:
    
    def add_documents(documents: List[DocumentModel]):
        try:
            document_objects = [
                Document(
                    page_content=doc.page_content, 
                    metadata=doc.metadata, 
                    id=str(doc.id) 
                ) 
                for doc in documents
            ]
            ids = [str(doc.id) for doc in documents]  
            
            collection__of__books.add_documents(documents=document_objects, ids=ids)
            
            return {"status": "Documents added successfully"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))




    def delete_document(id: str):
        try:
            collection__of__books.delete(ids=[id])
            return {"status": "Document deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Document with ID {id} not found")
    
    def update_document(document: Document):
        try:
            collection__of__books.update_document(document_id=document.id, document=document)
            return {"status": "Document updated successfully"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    def update_documents(ids: List[str], documents: List[Document]):
        if len(ids) != len(documents):
            raise HTTPException(status_code=400, detail="IDs and documents count mismatch")

        try:
            collection__of__books.update_documents(ids=ids, documents=documents)
            return {"status": "Documents updated successfully"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    def get_documents_by_ids(ids: List[str]):
        try:
            return  collection__of__books.get_by_ids(ids)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    def get_results(contentToSearch: str ):
        try:
            retriever = collection__of__books.as_retriever(
                search_type="similarity",
                #  search_kwargs={"k": 2},
            ) 
            
            return retriever.batch([contentToSearch])
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    def find_one(id: str ):
        try:
            
            return collection__of__books.get(id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
            
            
            


    # def add_document(document_model: DocumentModel):
    #     document = Document(
    #         page_content= document_model.page_content,
    #         metadata= document_model.metadata,
    #         id= document_model.id
    #     )
        
    #     type_of_document = document_model.type
        
    #     if type_of_document == "book":           
    #         return  vectorstore_of_books.add_documents(documents=[document], ids=[document.id])
            
    #     elif type_of_document == "thesis":     
    #         return  vectorstore_of_thesis.aadd_documents(documents=[document], ids=[document.id])
        
    # def delete_document(id: str, type: str):
    #     if type == "book":
    #         return vectorstore_of_books.delete(ids=[id])
        
    #     elif type == "thesis":
    #         return vectorstore_of_thesis.delete(ids=[id])
        
        
    
