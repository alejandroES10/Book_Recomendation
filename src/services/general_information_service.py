import os
import shutil
from typing import List
import uuid

from fastapi import File
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.database.chroma_database.general_information_collection import GeneralInformationCollection
from src.database.chroma_database.template_method import GeneralInformationProcessor
from src.interfaces.igeneral_information_service import IGeneralInformationService


class GeneralInformationService(IGeneralInformationService):
    def __init__(self):
        self.collection = GeneralInformationCollection()
    
    async def add_general_info(self,file_id: str, file: File) -> List[str]:
        extension = file.filename.lower().split('.')[-1]
        temp_file_path = f"temp_{file_id}.{extension}"


        try:
        # Save the uploaded file to a temporary file
            with open(temp_file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            processor = GeneralInformationProcessor(temp_file_path, {"file_id": file_id})
            await processor.process_and_store()


            return {"message": f"Información general del documento con file_id:{file_id} agregado corretamente"}
        
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)


    async def get_general_info_by_file_id(self, id: str) -> dict:
        return await self.collection.find_one(id)
        
        
    async def get_all_general_info(self) -> dict:
        return await self.collection.find_all()

    async def delete_general_info_by_file_id(self, id: str) -> None:
        return await self.collection.delete_documents(id)
