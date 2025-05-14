import os
import shutil
import uuid
from fastapi import APIRouter, File, HTTPException, UploadFile,Depends
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.api.services.chromadb_service import ChromaDBService
from src.api.services.general_information_service import GeneralInformationService
from src.database.chromadb.vector_store import collection_of_general_information
from src.api.security.auth import validate_api_key

router = APIRouter()

chroma_service = ChromaDBService(vector_store=collection_of_general_information)

general_info_service = GeneralInformationService()

@router.post("/", status_code=201,dependencies=[Depends(validate_api_key)])
async def create_documents_from_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    
    try:
       
       return await general_info_service.add_general_info(file)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
   


@router.delete("/{file_id}",dependencies=[Depends(validate_api_key)])
async def delete_document_by_file_id(file_id: str):
    try:
        await general_info_service.delete_general_info(file_id)
        return {"message": "Documents deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{id}",dependencies=[Depends(validate_api_key)])
async def get_document(id: str):
    try:
        document = await general_info_service.get_general_info_by_document_id(id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        return document
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/",dependencies=[Depends(validate_api_key)])
async def get_documents():
    try:
        return await general_info_service.get_all_general_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")