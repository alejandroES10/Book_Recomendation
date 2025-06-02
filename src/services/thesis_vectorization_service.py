
import asyncio
from typing import List
from src.database.chroma_database.thesis_collection import ThesisCollection
from src.database.postgres_database.thesis.process_status_repository import ProcessStatusRepository
from src.database.postgres_database.thesis.thesis_repository import ThesisRepository
from src.database.postgres_database.thesis.init_db import AsyncSessionLocal

from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


from src.interfaces.ithesis_vectorization_service import IThesisVectorizationService
from src.models.thesis_model import ProcessName, ProcessStatus
from src.schemas.thesis_schema import ThesisSchema

# class ThesisVectorizationService(IThesisVectorizationService):
#     def __init__(self, thesis_collection: ThesisCollection, thesis_repository: ThesisRepository):
#         self.thesis_collection = thesis_collection
#         self.thesis_repository = thesis_repository

#     async def vectorize_theses(self):
#         """
#         Recorre las tesis no procesadas, filtra las que no están vectorizadas,
#         las vectoriza y las marca como procesadas.
#         """
#         thesis_dtos = await self.extract_non_vectorized_theses()
#         success_count = 0
#         error_count = 0

#         for dto in thesis_dtos:
#             exists = await self.thesis_collection.exists_by_handle(dto.handle)
#             if exists:
#                 async with AsyncSessionLocal() as session:
#                     await self.thesis_repository.mark_as_vectorized(session, dto.handle)
#                 print(f"⏭️ Tesis ya vectorizada: {dto.handle}")
#                 continue

#             try:
#                 enriched_fragments = await self.process_thesis_to_fragments(dto)
#                 await self.thesis_collection.add_documents(enriched_fragments)

#                 # ✅ Marcar como procesada en la base de datos
#                 async with AsyncSessionLocal() as session:
#                     await self.thesis_repository.mark_as_vectorized(session, dto.handle)

#                 print(f"✅ Vectorizada y marcada como procesada: {dto.handle}")
#                 success_count += 1

#             except Exception as e:
#                 print(f"❌ Error procesando {dto.handle}: {e}")
#                 error_count += 1

#             print(f"\n📊 Resumen: {success_count} exitosas, {error_count} con error.")
        

#     async def extract_non_vectorized_theses(self):
#         """
#         Gets all unprocessed theses and converts them into ThesisDto objects.
#         """
#         async with AsyncSessionLocal() as session:
#             theses = await self.thesis_repository.get_non_vectorized_theses(session)

#         return [
#             ThesisSchema(
#                 handle=thesis.handle,
#                 metadata_json=thesis.metadata_json,
#                 original_name_document=thesis.original_name_document,
#                 size_bytes_document=thesis.size_bytes_document,
#                 download_url=thesis.download_url,
#                 is_processed=thesis.is_vectorized
#             )
#             for thesis in theses
#         ]


        
#     async def process_thesis_to_fragments(self, thesis_schema: ThesisSchema) -> List[Document]:
#             """
#             Procesa una tesis y devuelve sus fragmentos enriquecidos con metadatos.
#             """
#             loader = PyPDFLoader(thesis_schema.download_url)
#             documents = await loader.aload()
#             print("********Documento cargado********")
#             print(documents)

#             text_splitter = RecursiveCharacterTextSplitter(
#                 chunk_size=1000,
#                 chunk_overlap=100
#             )
#             splits = text_splitter.split_documents(documents)

#             enriched_documents = []
#             for fragment in splits:
#                 enriched_fragment = Document(
#                     page_content=fragment.page_content,
#                     metadata={
#                         "handle": thesis_schema.handle,
#                         "original_name_document": thesis_schema.original_name_document,
#                         "size_bytes_document": thesis_schema.size_bytes_document,
#                         **thesis_schema.metadata_json
#                     }
#                 )
#                 print("********Fragmento com metadatos********")
#                 print(enriched_fragment)
#                 enriched_documents.append(enriched_fragment)

#             return enriched_documents


class TesisError(Exception): pass
class CriticalProcessError(Exception): pass

class ThesisVectorizationService(IThesisVectorizationService):
    def __init__(
        self,
        thesis_collection: ThesisCollection,
        thesis_repository: ThesisRepository,
        process_status_repository: ProcessStatusRepository
    ):
        self.thesis_collection = thesis_collection
        self.thesis_repository = thesis_repository
        self.process_status_repository = process_status_repository

    async def vectorize_theses(self):
        success_count = 0
        error_messages = []

        try:
            async with AsyncSessionLocal() as session:
                await self.process_status_repository.set_status(
                    session,
                    process_name=ProcessName.VECTORIZE_THESIS,
                    status=ProcessStatus.RUNNING
                )

            non_vectorized_theses = await self.extract_non_vectorized_theses()

            for thesis in non_vectorized_theses:
                try:
                    exists = await self.thesis_collection.exists_by_handle(thesis.handle)
                    if exists:
                        async with AsyncSessionLocal() as session:
                            await self.thesis_repository.mark_as_vectorized(session, thesis.handle)
                        print(f"⏭️ Tesis ya vectorizada: {thesis.handle}")
                        continue

                    enriched_fragments = await self.process_thesis_to_fragments(thesis)
                    await self.thesis_collection.add_documents(enriched_fragments)

                    async with AsyncSessionLocal() as session:
                        await self.thesis_repository.mark_as_vectorized(session, thesis.handle)

                    print(f"✅ Vectorizada y marcada como procesada: {thesis.handle}")
                    success_count += 1

                except TesisError as e:
                    msg = f"Tesis {thesis.handle}: {str(e)}"
                    print(f"❌ {msg}")
                    error_messages.append(msg)
                    continue

                except Exception as e:
                    # Si ocurre un error inesperado grave, detenemos todo
                    raise CriticalProcessError(f"Fallo crítico al procesar {thesis.handle}: {e}")

            final_status = ProcessStatus.COMPLETED

        except CriticalProcessError as e:
            msg = f"[CRITICAL] {str(e)}"
            print(f"🛑 {msg}")
            error_messages.append(msg)
            final_status = ProcessStatus.FAILED

        except Exception as e:
            msg = f"[UNHANDLED] {str(e)}"
            print(f"🛑 {msg}")
            error_messages.append(msg)
            final_status = ProcessStatus.FAILED

        finally:
            async with AsyncSessionLocal() as session:
                await self.process_status_repository.set_status(
                    session,
                    process_name=ProcessName.VECTORIZE_THESIS,
                    status=final_status,
                    error_messages=error_messages
                )
            print(f"\n📊 Vectorización terminada. Éxitos: {success_count}, Errores: {len(error_messages)}")

    async def extract_non_vectorized_theses(self):
        async with AsyncSessionLocal() as session:
            theses = await self.thesis_repository.get_non_vectorized_theses(session)

        return [
            ThesisSchema(
                handle=thesis.handle,
                metadata_json=thesis.metadata_json,
                original_name_document=thesis.original_name_document,
                size_bytes_document=thesis.size_bytes_document,
                download_url=thesis.download_url,
                is_processed=thesis.is_vectorized
            )
            for thesis in theses
        ]

    def sanitize_metadata(self,metadata: dict) -> dict:
        sanitized = {}
        for key, value in metadata.items():
            if isinstance(value, (str, int, float, bool)):
                sanitized[key] = value
            elif isinstance(value, list):
                sanitized[key] = ", ".join(map(str, value))
            else:
                sanitized[key] = str(value)
        return sanitized

    async def process_thesis_to_fragments(self, thesis_schema: ThesisSchema) -> List[Document]:
        try:
            if not thesis_schema.download_url:
                raise TesisError("URL vacía")

            print("URL")
            print(thesis_schema.download_url)
            loader = PyPDFLoader(thesis_schema.download_url)
            documents = await loader.aload()

            if not documents:
                raise TesisError("No se pudo extraer contenido del PDF")

            print("********Documento cargado********")
            print(documents)

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=100
            )
            splits = text_splitter.split_documents(documents)

            enriched_documents = []
            sanitized_metadata = self.sanitize_metadata(thesis_schema.metadata_json)

            for fragment in splits:
                enriched_fragment = Document(
                    page_content=fragment.page_content,
                    metadata={
                        "handle": thesis_schema.handle,
                        "original_name_document": thesis_schema.original_name_document,
                        "size_bytes_document": thesis_schema.size_bytes_document,
                        **sanitized_metadata

                    }
                )
                print("********Fragmento con metadatos********")
                print(enriched_fragment)
                enriched_documents.append(enriched_fragment)

            return enriched_documents

        except Exception as e:
            raise TesisError(f"No se pudo procesar la tesis '{thesis_schema.handle}': {e}")
        
    async def get_vectorization_status(self) -> dict:
        async with AsyncSessionLocal() as session:
            status = await self.process_status_repository.get_status(session, ProcessName.VECTORIZE_THESIS)
            return status or {}
#*********************************** Test **************************************
# async def main():
#     thesis_collection = ThesisCollection()  # Instancia según tu implementación real
#     thesis_repository = ThesisRepository()

#     vectorization_service = ThesisVectorizationService(thesis_collection, thesis_repository)
    
#     await vectorization_service.vectorize_thesis()

     

# if __name__ == "__main__":
#     asyncio.run(main())