import os
import shutil
import uuid
from fastapi import APIRouter, File, HTTPException, UploadFile,Depends
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.api.services.chromadb_service import ChromaDBService
from src.database.vector_store import collection_of_general_information
from src.api.security.auth import validate_api_key

router = APIRouter()

chroma_service = ChromaDBService(vector_store=collection_of_general_information)


@router.post("/", status_code=201,dependencies=[Depends(validate_api_key)])
async def create_documents_from_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    temp_file_path = f"temp_{uuid.uuid4()}.pdf"
    
    try:
        # Save the uploaded file to a temporary file
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_id = str(uuid.uuid4())
        
        loader = PyPDFLoader(temp_file_path)
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )
        
        splits = text_splitter.split_documents(documents)
        
        for split in splits:
            split.metadata['file_id'] = file_id
        
        await chroma_service.add_documents(documents=splits)
        
        return {"file_id": file_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


@router.delete("/{file_id}",dependencies=[Depends(validate_api_key)])
async def delete_document_by_file_id(file_id: str):
    try:
        await chroma_service.delete_document_by_file_id(file_id)
        return {"message": "Documents deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{id}",dependencies=[Depends(validate_api_key)])
async def get_document(id: str):
    try:
        document = await chroma_service.find_one(id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        return document
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/",dependencies=[Depends(validate_api_key)])
async def get_documents():
    try:
        return await chroma_service.find_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")