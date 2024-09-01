from api.models.document_model import DocumentModel
from fastapi import APIRouter, HTTPException
from fastapi import APIRouter
from api.services.document_service import DocumentService
from langchain_core.documents import Document
from typing import List

router = APIRouter()


@router.post("/")
async def create_documents(documents: List[DocumentModel]):
    
    try:
        return DocumentService.add_documents(documents)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/{id}")
async def delete_document(id: str):
     try:
        return DocumentService.delete_document(id)
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
        return DocumentService.update_documents(ids=ids, documents=documents)
    except HTTPException as e:
        raise e
    
# @router.get("/documents/{ids}")
# async def find_documents(ids: List[str]):
#      try:
#         return DocumentService.get_documents_by_ids(ids)
#      except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/search/{contentToSearch}")
async def search_results(contentToSearch: str):
    return DocumentService.get_results(contentToSearch)
 
@router.get("/{id}") 
async def find_document(id: str):
    return DocumentService.find_one(id)


    
