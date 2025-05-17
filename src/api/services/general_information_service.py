import os
import shutil
from typing import List
import uuid

from fastapi import File
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.api.models.book_metadata_model import DocumentModel
from src.database.chromadb.general_information_collection import GeneralInformationCollection
from src.api.interfaces.igeneral_information_service import IGeneralInformationService


class GeneralInformationService(IGeneralInformationService):
    def __init__(self):
        self.collection = GeneralInformationCollection()
    
    async def add_general_info(self, file: File) -> List[str]:
        temp_file_path = f"temp_{uuid.uuid4()}.pdf"
    
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
        
        await self.collection.add_documents(splits)

        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
    
        return {"file_id": file_id}


    async def get_general_info_by_document_id(self, id: str) -> dict:
        return await self.collection.find_one(id)
    
    async def get_all_general_info(self) -> dict:
        return await self.collection.find_all()

    async def delete_general_info(self, id: str) -> None:
        return await self.collection.delete_documents(id)
