from database.vector_store import vectorstore_of_books
from database.vector_store import vectorstore_of_thesis
from langchain_core.documents import Document
from fastapi import HTTPException
from typing import List
from models.document_model import DocumentModel

class DocumentService:
    
    def add_documents(documents: List[Document]):
        try:
            ids = [doc.id for doc in documents]
            vectorstore_of_books.add_documents(documents=documents, ids=ids)
            return {"status": "Documents added successfully"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def delete_document(id: str):
        try:
            vectorstore_of_books.delete(ids=[id])
            return {"status": "Document deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Document with ID {id} not found")
    
    def update_document(document: Document):
        try:
            vectorstore_of_books.update_document(document_id=document.id, document=document)
            return {"status": "Document updated successfully"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    def update_documents(ids: List[str], documents: List[Document]):
        if len(ids) != len(documents):
            raise HTTPException(status_code=400, detail="IDs and documents count mismatch")

        try:
            vectorstore_of_books.update_documents(ids=ids, documents=documents)
            return {"status": "Documents updated successfully"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    def get_documents_by_ids(ids: List[str]):
        try:
            return  vectorstore_of_books.get_by_ids(ids)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    def get_results(contentToSearch: str ):
        try:
            retriever = vectorstore_of_books.as_retriever(
                search_type="similarity",
                #  search_kwargs={"k": 2},
            ) 
            return retriever.batch([contentToSearch])
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
        
        
    
