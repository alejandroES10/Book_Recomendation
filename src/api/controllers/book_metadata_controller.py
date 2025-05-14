from fastapi import APIRouter, HTTPException,Depends
from langchain_core.documents import Document
from typing import List
from src.api.models.document_model import BookMetadataModel, DocumentModel
from src.api.services.book_metadata_service import BookMetadataService
from src.api.services.chromadb_service import ChromaDBService
from src.database.chromadb.vector_store import collection_of_books
from src.api.security.auth import validate_api_key

router = APIRouter()

chroma_service = ChromaDBService(vector_store=collection_of_books)

book_metadata_service = BookMetadataService()

@router.post("/", status_code=201, dependencies=[Depends(validate_api_key)])
async def create_books(documents: List[BookMetadataModel]):
    try:
        await book_metadata_service.add_books(documents)
        return {"message": "Documents created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete_book("/{id}",dependencies=[Depends(validate_api_key)])
async def delete_document(id: str):
    try:
        await book_metadata_service.delete_book(id)
        return {"message": "Document deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/", dependencies=[Depends(validate_api_key)])
async def update_book(documents: List[BookMetadataModel]):
    try:
        await book_metadata_service.update_book(documents)
        return {"message": "Documents updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get_book("/{id}")
async def get_document(id: str):
    try:
        document = await book_metadata_service.get_book(id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        return document
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get_all_books("/")
async def get_documents():
    try:
        return await book_metadata_service.get_all_books()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")