
from abc import ABC
from typing import List, Optional, Tuple
from xml.dom.minidom import Document
from src.api.models.document_model import DocumentModel
from src.database.vector_store import collection_of_books, collection__of__thesis, collection_of_general_information

# class ChromaCollection(ABC):
     
#     def __init__(self):
#           super().__init__()
#           self._collection = None

#     def get_collection(name: str):
#          if name == 'collection_of_books': return collection_of_books
#          if name == 'collection_of_general_information': return collection_of_general_information
#          if name == 'collection_of_thesis': return collection__of__thesis
         
    
#     async def add_documents(self,elements):
#          pass
    
#     async def delete_documents(self,element_id): 
#          pass
    
#     async def update_documents(self,element):
#          pass
    
#     async def find_all(self):
#          pass
    
#     async def find_one(self,id):
#          pass
    
# #***************************************************************************

# class BookMetadata(ChromaCollection):
     
#     def __init__(self):
#         super().__init__()
#         self._collection = collection_of_books

#     async def add_element(self, models: List[DocumentModel]):
         
#         documents, ids = self._build_chroma_documents(models)

#         existing = self._collection._vector_store._collection.get(ids=ids)
#         if existing and len(existing['ids']) > 0:
#             raise ValueError("Duplicate ID found in the database")
        
#         try:
#             await self._collection._vector_store.aadd_documents(documents=documents, ids=ids)
#         except Exception as e:
#             raise ValueError(f"Failed to add documents: {str(e)}")
        

#     async def update_documents(self, models: List[DocumentModel]) -> None:
#         documents, ids = self._build_chroma_documents(models)

#         if len(documents) != len(ids):
#             raise ValueError("IDs and documents count mismatch")

#         await self._validate_ids_exist(ids)

#         try:
#             self._collection._vector_store.update_documents(ids=ids, documents=documents)
#         except Exception as e:
#             raise ValueError(f"Failed to update documents: {str(e)}")
        
#     async def delete_documents(self, id: str) -> None:
#         await self._validate_ids_exist([id])
#         try:
#             self._collection._vector_store.delete(ids=[id])
#         except Exception as e:
#             raise ValueError(f"Failed to delete document: {str(e)}")
        
#     async def find_one(self, id: str) -> Optional[dict]:
#         result = self._collection._vector_store.get(ids=[id])
#         if not result or not result['documents']:
#             return None
        
#     async def find_all(self) -> List[dict]:
#         result = self._collection._vector_store.get()
#         return [
#             {
#                 "id": id_,
#                 "metadata": self._extract_metadata_from_text(doc)
#             } for doc, id_ in zip(result['documents'], result['ids'])
#         ]

#     def _build_chroma_documents(self, models: List[DocumentModel]) -> Tuple[List[Document], List[str]]:
#         """Transforma modelos de entrada en objetos Document de LangChain"""
#         documents = []
#         ids = []

#         for model in models:
#             metadata_text = ". ".join(
#                 [f"{key.capitalize()}: {value}" for key, value in model.metadata.items()]
#             ) + "."

#             doc = Document(
#                 page_content=metadata_text,
#                 metadata={"fuente": "biblioteca_universitaria"},
#                 id=str(model.id)
#             )
#             documents.append(doc)
#             ids.append(str(model.id))

#         return documents, ids

#     def _extract_metadata_from_text(self, text: str) -> dict:
#         """
#         Convierte el texto del page_content de vuelta a un diccionario de metadatos.
#         Ejemplo de entrada:
#         "Título: Redes neuronales. Autor: Juan Pérez. Año: 2022."
#         """
#         metadata = {}
#         pairs = text.strip().split(". ")
#         for pair in pairs:
#             if ": " in pair:
#                 key, value = pair.split(": ", 1)
#                 metadata[key.lower()] = value.strip(".")
#         return metadata      

#     async def _validate_ids_exist(self, ids: List[str]) -> None:
#         """Verifica que todos los IDs existan en la colección"""
#         existing = self._collection._vector_store._collection.get(ids=ids)
#         if not existing or not existing.get("ids"):
#             raise ValueError("None of the provided IDs exist in the database")

#         existing_ids_set = set(existing["ids"])
#         missing_ids = [doc_id for doc_id in ids if doc_id not in existing_ids_set]

#         if missing_ids:
#             raise ValueError(f"The following IDs do not exist in the database: {', '.join(missing_ids)}")  
        
# #***************************************************************************

# class LibraryGeneralInformation(ChromaCollection):

#     def __init__(self):
#         super().__init__()
#         self._collection = collection_of_general_information

#     async def add_documents(self, documents: List[Document]) -> List[str]:
#         try:
#             return await self._collection._vector_store.aadd_documents(documents)
#         except Exception as e:
#             raise ValueError(f"Failed to add documents: {str(e)}")
        
#     async def delete_documents(self, file_id: str) -> None:
#         result = self._collection._vector_store._collection.delete(where={"file_id": file_id})
#         if not result:
#             raise ValueError(f"No documents found with file_id: {file_id}")
        
#     async def find_one(self):
#         result = self._collection._vector_store.get(ids=[id])
#         return result
    
#     async def find_all(self):
#         result = self._collection._vector_store.get()
#         return result

# #***************************************************************************

# class ThesisCollection(ChromaCollection):

#     def __init__(self):
#         super().__init__()
#         self._collection = collection__of__thesis


# # class ChromaService:
# #     def __init__(self, chroma_collection: ChromaCollection):
# #         self._chroma_collection = chroma_collection
        
# #     async def add(self,elements):
# #         return await self._chroma_collection.add_documents(elements)

# #     async def delete(self,element_id):
# #         return await self._chroma_collection.delete_documents(element_id)
    
# #     async def update(self,element):
# #         return await self._chroma_collection.update_documents(element)
    
# #     async def find_one(self,id):
# #         return self._chroma_collection.find_one(id)
    
# #     async def find_all(self, id):
# #         return self._chroma_collection.find_all()

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Tuple
from langchain_core.documents import Document
from src.api.models.document_model import DocumentModel


class ChromaCollection(ABC):
    """Clase abstracta base para todas las colecciones de Chroma."""

    def __init__(self):
        self._collection = None

    @abstractmethod
    async def add_documents(self, elements: List[Any]) -> List[str]:
        pass

    @abstractmethod
    async def delete_documents(self, element_id: str) -> None:
        pass

    @abstractmethod
    async def update_documents(self, elements: List[Any]) -> None:
        pass

    @abstractmethod
    async def find_all(self) -> List[Dict]:
        pass

    @abstractmethod
    async def find_one(self, id: str) -> Optional[Dict]:
        pass


class BookMetadata(ChromaCollection):
    """Colección especializada en libros con metadatos."""

    def __init__(self):
        super().__init__()
        self._collection = collection_of_books

    def _build_chroma_documents(self, models: List[DocumentModel]) -> Tuple[List[Document], List[str]]:
        documents = []
        ids = []
        for model in models:
            metadata_text = ". ".join([f"{k.capitalize()}: {v}" for k, v in model.metadata.items()]) + "."
            documents.append(Document(
                page_content=metadata_text,
                metadata={"fuente": "biblioteca_universitaria"},
                id=str(model.id)
            ))
            ids.append(str(model.id))
        return documents, ids

    def _extract_metadata_from_text(self, text: str) -> dict:
        metadata = {}
        for item in text.strip().split(". "):
            if ": " in item:
                key, value = item.split(": ", 1)
                metadata[key.lower()] = value.strip(".")
        return metadata

    async def _validate_ids_exist(self, ids: List[str]) -> None:
        result = self._collection._vector_store._collection.get(ids=ids)
        if not result or not result.get("ids"):
            raise ValueError("IDs no encontrados en la base de datos")
        missing = [i for i in ids if i not in result["ids"]]
        if missing:
            raise ValueError(f"IDs faltantes en la base de datos: {', '.join(missing)}")

    async def add_documents(self, models: List[DocumentModel]) -> List[str]:
        documents, ids = self._build_chroma_documents(models)
        existing = self._collection._vector_store._collection.get(ids=ids)
        if existing and existing.get("ids"):
            raise ValueError("IDs duplicados encontrados en la base de datos")
        try:
            return await self._collection._vector_store.aadd_documents(documents=documents, ids=ids)
        except Exception as e:
            raise ValueError(f"Error al añadir documentos: {e}")

    async def update_documents(self, models: List[DocumentModel]) -> None:
        documents, ids = self._build_chroma_documents(models)
        if len(documents) != len(ids):
            raise ValueError("Cantidad de documentos y de IDs no coinciden")
        await self._validate_ids_exist(ids)
        try:
            self._collection._vector_store.update_documents(ids=ids, documents=documents)
        except Exception as e:
            raise ValueError(f"Error al actualizar documentos: {e}")

    async def delete_documents(self, id: str) -> None:
        await self._validate_ids_exist([id])
        try:
            self._collection._vector_store.delete(ids=[id])
        except Exception as e:
            raise ValueError(f"Error al eliminar el documento: {e}")

    async def find_one(self, id: str) -> Optional[dict]:
        result = self._collection._vector_store.get(ids=[id])
        if not result or not result.get('documents'):
            return None
        return {
            "id": result["ids"][0],
            "metadata": self._extract_metadata_from_text(result["documents"][0])
        }

    async def find_all(self) -> List[dict]:
        result = self._collection._vector_store.get()
        return [{
            "id": id_,
            "metadata": self._extract_metadata_from_text(doc)
        } for doc, id_ in zip(result["documents"], result["ids"])]


class LibraryGeneralInformation(ChromaCollection):
    """Colección para documentos de información general."""

    def __init__(self):
        super().__init__()
        self._collection = collection_of_general_information

    async def add_documents(self, documents: List[Document]) -> List[str]:
        try:
            return await self._collection._vector_store.aadd_documents(documents)
        except Exception as e:
            raise ValueError(f"Error al añadir documentos: {e}")

    async def delete_documents(self, file_id: str) -> None:
        deleted = self._collection._vector_store._collection.delete(where={"file_id": file_id})
        if not deleted:
            raise ValueError(f"No se encontraron documentos con file_id: {file_id}")

    async def find_one(self, id: str) -> Optional[dict]:
        result = self._collection._vector_store.get(ids=[id])
        if not result or not result.get('documents'):
            return None
        return {
            "id": result["ids"][0],
            "content": result["documents"][0],
            "metadata": result["metadatas"][0] if result.get("metadatas") else {}
        }

    async def find_all(self) -> List[dict]:
        result = self._collection._vector_store.get()
        return [{
            "id": id_,
            "content": doc,
            "metadata": meta
        } for doc, meta, id_ in zip(result["documents"], result["metadatas"], result["ids"])]

    async def update_documents(self, elements: List[DocumentModel]) -> None:
        raise NotImplementedError("No se permite actualización en esta colección")


class ThesisCollection(ChromaCollection):
    """Colección para tesis académicas."""

    def __init__(self):
        super().__init__()
        self._collection = collection__of__thesis

    async def add_documents(self, documents: List[Document]) -> List[str]:
        try:
            return await self._collection._vector_store.aadd_documents(documents)
        except Exception as e:
            raise ValueError(f"Error al añadir documentos: {e}")

    async def delete_documents(self, id: str) -> None:
        try:
            self._collection._vector_store.delete(ids=[id])
        except Exception as e:
            raise ValueError(f"Error al eliminar documento: {e}")

    async def update_documents(self, documents: List[Document]) -> None:
        try:
            ids = [doc.id for doc in documents]
            self._collection._vector_store.update_documents(ids=ids, documents=documents)
        except Exception as e:
            raise ValueError(f"Error al actualizar documentos: {e}")

    async def find_one(self, id: str) -> Optional[dict]:
        result = self._collection._vector_store.get(ids=[id])
        if not result or not result.get('documents'):
            return None
        return {
            "id": result["ids"][0],
            "content": result["documents"][0],
            "metadata": result["metadatas"][0] if result.get("metadatas") else {}
        }

    async def find_all(self) -> List[dict]:
        result = self._collection._vector_store.get()
        return [{
            "id": id_,
            "content": doc,
            "metadata": meta
        } for doc, meta, id_ in zip(result["documents"], result["metadatas"], result["ids"])]


# Función para obtener la colección correspondiente por nombre
def get_collection(name: str) -> Optional[ChromaCollection]:
    collections = {
        'collection_of_books': BookMetadata(),
        'collection_of_general_information': LibraryGeneralInformation(),
        'collection_of_thesis': ThesisCollection()
    }
    return collections.get(name)


from typing import List
from src.api.models.document_model import DocumentModel

class BookService:
    def __init__(self):
        self.collection = BookMetadata()
    
    async def add_books(self, models: List[DocumentModel]) -> List[str]:
        return await self.collection.add_documents(models)

    async def get_book(self, id: str) -> dict:
        return await self.collection.find_one(id)

    async def delete_book(self, id: str) -> None:
        return await self.collection.delete_documents(id)

    async def update_book(self, id: str, model: DocumentModel) -> None:
        return await self.collection.update_document(id, model)

from typing import List
from src.api.models.document_model import DocumentModel


class GeneralInformationService:
    def __init__(self):
        self.collection = LibraryGeneralInformation()
    
    async def add_general_info(self, models: List[DocumentModel]) -> List[str]:
        return await self.collection.add_documents(models)

    async def get_general_info(self, id: str) -> dict:
        return await self.collection.find_one(id)

    async def delete_general_info(self, id: str) -> None:
        return await self.collection.delete_documents(id)


from typing import List
from src.api.models.document_model import DocumentModel

class ThesisService:
    def __init__(self):
        self.collection = ThesisCollection()
    
    async def add_theses(self, models: List[DocumentModel]) -> List[str]:
        return await self.collection.add_documents(models)

    async def get_thesis(self, id: str) -> dict:
        return await self.collection.find_one(id)

    async def delete_thesis(self, id: str) -> None:
        return await self.collection.delete_documents(id)
