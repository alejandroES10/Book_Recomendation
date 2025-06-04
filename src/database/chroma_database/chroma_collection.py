
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from langchain_core.documents import Document




# class ChromaCollection(ABC):
#     """Clase abstracta base para todas las colecciones de Chroma."""

#     # def __init__(self):
#     #     self._collection = None

#     @abstractmethod
#     async def add_documents(self, documents: List[Document], ids:Optional[List[str]]) -> List[str]:
#         pass


#     @abstractmethod
#     async def delete_documents(self, document_id: str) -> None:
#         pass

#     @abstractmethod
#     async def update_documents(self, documents: List[Document], ids:Optional[List[str]]) -> None:
#         pass

#     @abstractmethod
#     async def find_all(self) -> List[Dict]:
#         pass

#     @abstractmethod
#     async def find_one(self, document_id: str) -> Optional[Dict]:
#         pass


class BaseCollection(ABC):
    def __init__(self, collection):
        self._collection = collection

    @abstractmethod
    async def add_documents(self, *args, **kwargs):
        pass

    @abstractmethod
    async def delete_documents(self, *args, **kwargs):
        pass

    @abstractmethod
    async def find_one(self, *args, **kwargs):
        pass

    @abstractmethod
    async def find_all(self):
        pass

    def _validate_identifier(self, identifier: str):
        if not identifier or not identifier.strip():
            raise ValueError("El identificador no puede estar vacío")

    def _validate_documents(self, documents: List[Document]):
        if not documents:
            raise ValueError("La lista de documentos no puede estar vacía")

class BaseDocumentCollection(BaseCollection, ABC):

    @abstractmethod
    def _build_filter(self, identifier: str) -> dict:
        pass

    async def _check_exists(self, identifier: str) -> bool:
        self._validate_identifier(identifier)
        try:
            result = self._collection.get(where=self._build_filter(identifier))
            return bool(result and result.get("ids"))
        except Exception as e:
            raise ValueError(f"Error al verificar existencia del documento '{identifier}': {e}")

    async def add_documents(self, identifier: str, documents: List[Document]) -> List[str]:
        self._validate_identifier(identifier)
        self._validate_documents(documents)
        try:
            if not await self._check_exists(identifier):
                return await self._collection.aadd_documents(documents)
            raise ValueError(f"Ya existe información vectorizada para el identificador: {identifier}")
        except Exception as e:
            raise ValueError(f"Error al añadir documentos: {e}")

    async def delete_documents(self, identifier: str) -> None:
        self._validate_identifier(identifier)
        if await self._check_exists(identifier):
            self._collection._collection.delete(where=self._build_filter(identifier))
        else:
            raise ValueError(f"No existe información vectorizada con el identificador: {identifier}")

    async def get_results(self, identifier: str) -> dict:
        self._validate_identifier(identifier)
        return self._collection.get(where=self._build_filter(identifier))

    def _format_results(self, result: dict) -> List[dict]:
        return [
            {"id": id_, "content": doc, "metadata": meta}
            for doc, meta, id_ in zip(result["documents"], result["metadatas"], result["ids"])
        ]

    async def find_one(self, identifier: str) -> List[dict]:
        self._validate_identifier(identifier)
        result = await self.get_results(identifier)
        if not result or not result.get("ids"):
            raise ValueError(f"No existe información vectorizada para el identificador: {identifier}")
        return self._format_results(result)

    async def find_all(self) -> List[dict]:
        result = self._collection.get()
        return self._format_results(result)
    

    #Metodo para testear
    async def count_distinct_identifiers(self) -> int:
        """Cuenta cuántos identificadores únicos hay en la colección."""
        try:
            result = self._collection.get()
            metadatas = result.get("metadatas", [])

            # Detectar la clave usada como identificador
            filter_example = self._build_filter("ejemplo")
            if not filter_example:
                raise ValueError("El método _build_filter no define ninguna clave para el identificador")

            identifier_key = next(iter(filter_example.keys()))

            # Extraer todos los valores de esa clave y contar únicos
            identifiers = {
                metadata.get(identifier_key)
                for metadata in metadatas
                if metadata.get(identifier_key)
            }

            return len(identifiers)

        except Exception as e:
            raise ValueError(f"Error al contar identificadores únicos: {e}")


# class BaseDocumentCollection(BaseCollection):
    
#     @abstractmethod
#     def _build_filter(self, identifier: str) -> dict:
#         """Construye el filtro para búsquedas y operaciones."""
#         pass

#     async def _check_exists(self, identifier: str) -> bool:
#         try:
#             result = self._collection.get(where=self._build_filter(identifier))
#             return bool(result and result.get("ids"))
#         except Exception as e:
#             raise ValueError(f"Error al verificar existencia del documento '{identifier}': {e}")

#     async def add_documents(self, identifier: str, documents: List[Document]) -> List[str]:
#         try:
#             if not await self._check_exists(identifier):
#                 return await self._collection.aadd_documents(documents)
#             raise ValueError(f"Ya existe información vectorizada para el identificador: {identifier}")
#         except Exception as e:
#             raise ValueError(f"Error al añadir documentos: {e}")

#     async def delete_documents(self, identifier: str) -> None:
#         if await self._check_exists(identifier):
#             self._collection._collection.delete(where=self._build_filter(identifier))
#         else:
#             raise ValueError(f"No existe información vectorizada con el identificador: {identifier}")

#     async def get_results(self, identifier: str) -> dict:
#         return self._collection.get(where=self._build_filter(identifier))

#     def _format_results(self, result: dict) -> List[dict]:
#         return [
#             {"id": id_, "content": doc, "metadata": meta}
#             for doc, meta, id_ in zip(result["documents"], result["metadatas"], result["ids"])
#         ]

#     async def find_one(self, identifier: str) -> List[dict]:
#         result = await self.get_results(identifier)
#         if not result or not result.get("ids"):
#             raise ValueError(f"No existe información vectorizada para el identificador: {identifier}")
#         return self._format_results(result)

#     async def find_all(self) -> List[dict]:
#         result = self._collection.get()
#         return self._format_results(result)
