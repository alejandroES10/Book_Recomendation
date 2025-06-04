from abc import ABC, abstractmethod
from typing import List
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders.base import BaseLoader

from src.database.chroma_database.general_information_collection import GeneralInformationCollection
from src.database.chroma_database.thesis_collection import ThesisCollection
from .chroma_collection import BaseDocumentCollection  # ajusta según tu estructura real
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader

class BaseDocumentProcessor(ABC):
    def __init__(self, path_or_url: str, metadata: dict):
        if not path_or_url or not isinstance(path_or_url, str):
            raise ValueError("El parámetro 'path_or_url' no puede estar vacío y debe ser una cadena no vacía.")

        if not metadata or not isinstance(metadata, dict):
             raise ValueError("El parámetro 'metadata' no puede estar vacío y debe ser un diccionario.")
        self.path_or_url = path_or_url
        self.metadata = metadata

    async def process_and_store(self) -> List[str]:
        loader = self.get_loader()
        documents = await loader.aload()

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        splits = splitter.split_documents(documents)

        for fragment in splits:
            fragment.metadata.update(self.metadata)

        collection = self.get_collection()
        identifier = self.get_identifier()

        return await collection.add_documents(identifier=identifier, documents=splits)

    @abstractmethod
    def get_loader(self) -> BaseLoader:
        pass

    @abstractmethod
    def get_collection(self) -> BaseDocumentCollection:
        pass

    @abstractmethod
    def get_identifier(self) -> str:
        pass


class ThesisProcessor(BaseDocumentProcessor):
    def get_loader(self):
        return PyPDFLoader(self.path_or_url)

    def get_collection(self):
        return ThesisCollection()

    def get_identifier(self) -> str:
        return self.metadata["handle"]
    
class GeneralInformationProcessor(BaseDocumentProcessor):
    def get_loader(self):
        if self.path_or_url.lower().endswith(".pdf"):
            return PyPDFLoader(self.path_or_url)
        elif self.path_or_url.lower().endswith(".docx"):
            return Docx2txtLoader(self.path_or_url)
        else:
            raise ValueError("Formato de archivo no soportado")

    def get_collection(self):
        return GeneralInformationCollection()

    def get_identifier(self) -> str:
        return self.metadata["file_id"]