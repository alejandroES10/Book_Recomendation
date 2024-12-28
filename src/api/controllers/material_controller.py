from src.api.models.document_model import DocumentModel
from src.api.models.search_model import SearchModel
from fastapi import APIRouter, HTTPException, Query

# from fastapi import APIRouter
from src.api.services.chromadb_service import ChromaDBService
from src.api.services.document_service import DocumentService
from langchain_core.documents import Document
from typing import List,Optional
from src.database.vector_store import  collection__of__books

router = APIRouter()

colection = collection__of__books
chroma_service =  ChromaDBService(vectore_store = colection)

@router.post("/")
async def create_documents(documents: List[DocumentModel]):
    
    try:
        return chroma_service.add_document(documents)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/{id}")
async def delete_document(id: str):
     try:
        return chroma_service.delete_document_by_id(id)
     except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# @router.put("/documents/{id}")
# async def update_document(document: Document):
#     try:
#         return DocumentService.update_document(document_id=document.id, document=document)
#     except HTTPException as e:
#         raise e

@router.put("/")
async def update_documents(documents: List[DocumentModel]):
    ids = [doc.id for doc in documents]
    
    try:
        return chroma_service.update_documents(ids=ids, documents=documents)
    except HTTPException as e:
        raise e
    
# @router.get("/documents/{ids}")
# async def find_documents(ids: List[str]):
#      try:
#         return DocumentService.get_documents_by_ids(ids)
#      except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
    
# @router.get("/search/")
# async def search_results(content: str = Query(...), k_results: Optional[int] = Query(10)):
#     return DocumentService.get_results(content, k_results)
 
@router.get("/{id}") 
async def get_document(id: str):
    return chroma_service.find_one(id)

@router.get("/") 
async def get_documents():
    return chroma_service.find_all()


    
