import os
import shutil
import uuid
from src.api.models.document_model import DocumentModel
from src.api.models.search_model import SearchModel
from fastapi import APIRouter, File, HTTPException, Query, UploadFile

# from fastapi import APIRouter
from src.api.services.document_service import DocumentService
from src.api.services.chromadb_service import ChromaDBService
from langchain_core.documents import Document
from typing import List,Optional
from src.database.vector_store import  collection__of__general_information
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

router = APIRouter()

colection = collection__of__general_information
chroma_service =  ChromaDBService(collection= colection)

@router.post("/")
async def create_documents_of_general_information(file: UploadFile = File(...)):
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension != '.pdf':
        raise HTTPException(status_code=400, detail=f"Unsupported file type.")
    
    temp_file_path = f"temp_{file.filename}"

    try:
        # Save the uploaded file to a temporary file
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # file_id = str(uuid.uuid4())
        file_id = uuid.uuid4()
        
        loader = PyPDFLoader(temp_file_path)
        
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500, 
            chunk_overlap=150 

            )
        
        splits = text_splitter.split_documents(documents)
        
        for split in splits:
            split.metadata['file_id'] = file_id.int
            
        return  chroma_service.add_document( documents= splits)      

     
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


    
    # try:
    #     return chroma_service.add_document()
    # except Exception as e:
    #     raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/{id}")
async def delete_document(id: str):
     try:
        return chroma_service.delete_document(id)
     except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    


# @router.put("/")
# async def update_documents(documents: List[DocumentModel]):
#     ids = [doc.id for doc in documents]
    
#     try:
#         return DocumentService.update_documents(ids=ids, documents=documents)
#     except HTTPException as e:
#         raise e
    

    
# @router.get("/search/")
# async def search_results(content: str = Query(...), k_results: Optional[int] = Query(10)):
#     return DocumentService.get_results(content, k_results)
 
@router.get("/{id}") 
async def get_document(id: str):
    return chroma_service.find_one(id)

@router.get("/") 
async def get_documents():
    return chroma_service.find_all()


    
