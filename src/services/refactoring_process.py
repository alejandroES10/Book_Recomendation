# from abc import ABC, abstractmethod
# from dataclasses import dataclass
# from typing import List, Dict, Optional, Protocol
# from pydantic import BaseModel
# import logging

# # Configuración de logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # --------------------------
# # Modelos y DTOs
# # --------------------------
# class ThesisSchema(BaseModel):
#     handle: str
#     metadata_json: dict
#     original_name_document: str
#     size_bytes_document: int
#     download_url: str
#     is_vectorized: bool

# @dataclass
# class ProcessResult:
#     success_count: int = 0
#     error_messages: List[str] = None

#     def __post_init__(self):
#         self.error_messages = self.error_messages or []

# # --------------------------
# # Interfaces
# # --------------------------
# class IURLBuilder(Protocol):
#     def build_url(self, item, bitstream) -> str:
#         ...

# class IThesisDataImporterService(ABC):
#     @abstractmethod
#     async def upsert_theses(self) -> ProcessResult:
#         pass

#     @abstractmethod
#     async def get_import_status(self) -> dict:
#         pass

# class IThesisVectorizationService(ABC):
#     @abstractmethod
#     async def vectorize_theses(self) -> ProcessResult:
#         pass

#     @abstractmethod
#     async def get_vectorization_status(self) -> dict:
#         pass

# # --------------------------
# # Implementación del Factory para URLs
# # --------------------------
# @dataclass
# class APIURLBuilder:
#     base_url: str = "https://repositorio.cujae.edu.cu/server/api/core/bitstreams"

#     def build_url(self, _, bitstream) -> str:
#         return f"{self.base_url}/{bitstream.uuid}/content"

# @dataclass
# class HandleURLBuilder:
#     base_url: str = "http://tesis.cujae.edu.cu/bitstream/handle"

#     def build_url(self, item, bitstream) -> str:
#         return f"{self.base_url}/{item.handle}/{bitstream.name}?sequence=1&isAllowed=y"

# class URLBuilderFactory:
#     @staticmethod
#     def create_builder(builder_type: str) -> IURLBuilder:
#         builders = {
#             "api": APIURLBuilder(),
#             "handle": HandleURLBuilder()
#         }
#         return builders.get(builder_type, APIURLBuilder())  # Default API

# # --------------------------
# # Implementación de servicios
# # --------------------------
# class ThesisDataImporterService(IThesisDataImporterService):
#     def __init__(
#         self,
#         dspace_service,
#         thesis_repository,
#         process_status_repository,
#         url_builder: IURLBuilder = None,
#         community_name: str = "tesis",
#         batch_size: int = 100
#     ):
#         self.dspace_service = dspace_service
#         self.thesis_repository = thesis_repository
#         self.process_status_repository = process_status_repository
#         self.url_builder = url_builder or URLBuilderFactory.create_builder("api")
#         self.community_name = community_name
#         self.batch_size = batch_size

#     async def upsert_theses(self) -> ProcessResult:
#         result = ProcessResult()
#         process_name = ProcessName.IMPORT_THESIS

#         async with AsyncSessionLocal() as session:
#             try:
#                 await self._update_process_status(session, process_name, ProcessStatus.RUNNING)
                
#                 items = await self._fetch_items()
#                 if not items:
#                     await self._update_process_status(session, process_name, ProcessStatus.COMPLETED)
#                     logger.info("No se encontraron ítems en la comunidad.")
#                     return result

#                 result = await self._process_items(items)
#                 await self._update_process_status(session, process_name, ProcessStatus.COMPLETED)
#                 logger.info(f"Proceso completado. Tesis procesadas: {result.success_count}")

#             except Exception as e:
#                 await self._handle_error(session, process_name, str(e))
#                 raise

#         return result

#     async def get_import_status(self) -> dict:
#         async with AsyncSessionLocal() as session:
#             return await self.process_status_repository.get_status(session, ProcessName.IMPORT_THESIS) or {}

#     # --------------------------
#     # Métodos privados
#     # --------------------------
#     async def _fetch_items(self) -> List:
#         return await self.dspace_service.get_items_by_top_community_name(
#             self.community_name, 
#             limit=self.batch_size
#         )

#     async def _process_items(self, items: List) -> ProcessResult:
#         result = ProcessResult()
        
#         for item in items:
#             try:
#                 if await self._process_item(item):
#                     result.success_count += 1
#             except Exception as e:
#                 handle = getattr(item, 'handle', 'unknown')
#                 error_msg = f"Error procesando ítem '{handle}': {e}"
#                 result.error_messages.append(error_msg)
#                 logger.error(error_msg)

#         return result

#     async def _process_item(self, item) -> bool:
#         bitstream = await self._find_valid_bitstream(item)
#         if not bitstream:
#             return False

#         pdf_url = self.url_builder.build_url(item, bitstream)
#         thesis_schema = self._build_thesis_schema(item, bitstream, pdf_url)
        
#         async with AsyncSessionLocal() as session:
#             await self.thesis_repository.upsert_thesis(session, thesis_schema)
        
#         return True

#     async def _find_valid_bitstream(self, item) -> Optional:
#         bundles = await self.dspace_service.get_bundles_by_item(item)
#         original_bundle = next((b for b in bundles if getattr(b, "name", "").upper() == "ORIGINAL"), None)
        
#         if not original_bundle:
#             return None
            
#         bitstreams = await self.dspace_service.get_bitstreams_by_bundle(original_bundle)
#         return bitstreams[0] if bitstreams else None

#     def _build_thesis_schema(self, item, bitstream, pdf_url) -> ThesisSchema:
#         return ThesisSchema(
#             handle=item.handle,
#             metadata_json=self._clean_metadata(item.metadata),
#             original_name_document=bitstream.name,
#             size_bytes_document=bitstream.sizeBytes,
#             download_url=pdf_url,
#             is_vectorized=False
#         )

#     def _clean_metadata(self, metadata: dict) -> dict:
#         return {
#             key: values[0] if len(values := [entry["value"] for entry in entries if "value" in entry]) == 1 else values
#             for key, entries in metadata.items()
#             if key not in {"dc.description.abstract"}
#         }

#     async def _update_process_status(self, session, process_name, status, errors=None):
#         await self.process_status_repository.set_status(
#             session,
#             process_name,
#             status,
#             error_messages=errors
#         )

#     async def _handle_error(self, session, process_name, error_msg):
#         logger.error(f"Proceso de importación fallido: {error_msg}")
#         await self._update_process_status(
#             session,
#             process_name,
#             ProcessStatus.FAILED,
#             errors=[error_msg]
#         )


# class ThesisVectorizationService(IThesisVectorizationService):
#     def __init__(
#         self,
#         thesis_collection,
#         thesis_repository,
#         process_status_repository,
#         chunk_size: int = 1000,
#         chunk_overlap: int = 100
#     ):
#         self.thesis_collection = thesis_collection
#         self.thesis_repository = thesis_repository
#         self.process_status_repository = process_status_repository
#         self.chunk_size = chunk_size
#         self.chunk_overlap = chunk_overlap

#     async def vectorize_theses(self) -> ProcessResult:
#         result = ProcessResult()
        
#         try:
#             async with AsyncSessionLocal() as session:
#                 await self._update_process_status(session, ProcessName.VECTORIZE_THESIS, ProcessStatus.RUNNING)

#             theses = await self._get_non_vectorized_theses()
#             result = await self._process_theses(theses)

#             final_status = ProcessStatus.COMPLETED if not result.error_messages else ProcessStatus.FAILED
#             await self._update_process_status(session, ProcessName.VECTORIZE_THESIS, final_status, result.error_messages)

#         except Exception as e:
#             error_msg = f"Error crítico: {str(e)}"
#             result.error_messages.append(error_msg)
#             logger.error(error_msg)
#             await self._update_process_status(session, ProcessName.VECTORIZE_THESIS, ProcessStatus.FAILED, [error_msg])
#             raise

#         finally:
#             logger.info(f"Vectorización terminada. Éxitos: {result.success_count}, Errores: {len(result.error_messages)}")
#             return result

#     async def get_vectorization_status(self) -> dict:
#         async with AsyncSessionLocal() as session:
#             return await self.process_status_repository.get_status(session, ProcessName.VECTORIZE_THESIS) or {}

#     # --------------------------
#     # Métodos privados
#     # --------------------------
#     async def _get_non_vectorized_theses(self) -> List[ThesisSchema]:
#         async with AsyncSessionLocal() as session:
#             db_theses = await self.thesis_repository.get_non_vectorized_theses(session)
#             return [ThesisSchema(**thesis.__dict__) for thesis in db_theses]

#     async def _process_theses(self, theses: List[ThesisSchema]) -> ProcessResult:
#         result = ProcessResult()
        
#         for thesis in theses:
#             try:
#                 if await self.thesis_collection.exists_by_handle(thesis.handle):
#                     await self._mark_as_vectorized(thesis.handle)
#                     logger.info(f"Tesis ya vectorizada: {thesis.handle}")
#                     continue

#                 fragments = await self._process_thesis_fragments(thesis)
#                 await self.thesis_collection.add_documents(fragments)
#                 await self._mark_as_vectorized(thesis.handle)
                
#                 result.success_count += 1
#                 logger.info(f"Tesis vectorizada: {thesis.handle}")

#             except Exception as e:
#                 error_msg = f"Error procesando tesis {thesis.handle}: {str(e)}"
#                 result.error_messages.append(error_msg)
#                 logger.error(error_msg)

#         return result

#     async def _process_thesis_fragments(self, thesis: ThesisSchema) -> List[Document]:
#         if not thesis.download_url:
#             raise ValueError("URL de descarga vacía")

#         loader = PyPDFLoader(thesis.download_url)
#         documents = await loader.aload()
        
#         if not documents:
#             raise ValueError("No se pudo extraer contenido del PDF")

#         splitter = RecursiveCharacterTextSplitter(
#             chunk_size=self.chunk_size,
#             chunk_overlap=self.chunk_overlap
#         )
        
#         return [
#             Document(
#                 page_content=fragment.page_content,
#                 metadata=self._build_fragment_metadata(thesis, fragment)
#             )
#             for fragment in splitter.split_documents(documents)
#         ]

#     def _build_fragment_metadata(self, thesis: ThesisSchema, fragment) -> Dict:
#         return {
#             "handle": thesis.handle,
#             "original_name_document": thesis.original_name_document,
#             "size_bytes_document": thesis.size_bytes_document,
#             **self._sanitize_metadata(thesis.metadata_json)
#         }

#     def _sanitize_metadata(self, metadata: dict) -> dict:
#         return {
#             key: ", ".join(map(str, value)) if isinstance(value, list) else value
#             for key, value in metadata.items()
#             if isinstance(value, (str, int, float, bool, list))
#         }

#     async def _mark_as_vectorized(self, handle: str):
#         async with AsyncSessionLocal() as session:
#             await self.thesis_repository.mark_as_vectorized(session, handle)

#     async def _update_process_status(self, session, process_name, status, errors=None):
#         await self.process_status_repository.set_status(
#             session,
#             process_name,
#             status,
#             error_messages=errors
#         )