from abc import ABC, abstractmethod
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders.base import BaseLoader
from src.database.chroma_database.general_information_collection import GeneralInformationCollection
from src.database.chroma_database.thesis_collection import ThesisCollection
from .chroma_collection import BaseDocumentCollection  
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
import aiohttp
import tempfile
import ssl



class BaseDocumentProcessor(ABC):
    def __init__(self, path_or_url: str, metadata: dict):
        if not path_or_url or not isinstance(path_or_url, str):
            raise ValueError("El parámetro 'path_or_url' no puede estar vacío y debe ser una cadena no vacía.")

        if not metadata or not isinstance(metadata, dict):
             raise ValueError("El parámetro 'metadata' no puede estar vacío y debe ser un diccionario.")
        self.path_or_url = path_or_url
        self.metadata = metadata

    async def process_and_store(self):
        path = None

        try:
        
            path = await self.get_path()
           
            loader = self.get_loader(path)
            
            documents = await loader.aload()

            
            splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
            splits = splitter.split_documents(documents)

            for fragment in splits:
                # fragment.metadata.update(self.metadata)
                # fragment.metadata = self.metadata
                fragment.metadata = self.clean_metadata(self.metadata)
                

            collection = self.get_collection()
            identifier = self.get_identifier()

            return await collection.add_documents(identifier=identifier, documents=splits)
        
       

        finally:    
            if path and os.path.exists(path):
                os.remove(path)
        
    
    @abstractmethod
    def get_loader(self) -> BaseLoader:
        pass

    @abstractmethod
    async def get_path(self) -> str:
        pass

    @abstractmethod
    def get_collection(self) -> BaseDocumentCollection:
        pass

    @abstractmethod
    def get_identifier(self) -> str:
        pass

    def clean_metadata(self,metadata: dict) -> dict:
        
        return {
            k: v if isinstance(v, (str, int, float, bool, type(None))) else str(v)
            for k, v in metadata.items()
        }
    

class GeneralInformationProcessor(BaseDocumentProcessor):
    def get_loader(self,path: str):
        if self.path_or_url.lower().endswith(".pdf"):
            return PyPDFLoader(path)
        elif self.path_or_url.lower().endswith(".docx"):
            return Docx2txtLoader(path)
        else:
            raise ValueError("Formato de archivo no soportado")

    def get_collection(self):
        return GeneralInformationCollection()

    def get_identifier(self) -> str:
        return self.metadata["file_id"]
    
    async def get_path(self):
        return self.path_or_url
    
    
class ThesisProcessor(BaseDocumentProcessor):
    def get_loader(self, path: str) -> BaseLoader:
        return PyPDFLoader(path)

    def get_collection(self):
        return ThesisCollection()

    def get_identifier(self) -> str:
        print(self.metadata)
        return self.metadata["handle"]
    
    async def get_path(self):
        return await self.download_pdf(self.path_or_url)


   


    async def download_pdf(self,url: str, timeout_sec: int = 100) -> str:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        timeout = aiohttp.ClientTimeout(total=timeout_sec)
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context), timeout=timeout) as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    raise Exception(f"Error {resp.status} al descargar el PDF")

                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                with open(tmp.name, "wb") as f:
                    while True:
                        chunk = await resp.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)
                return tmp.name