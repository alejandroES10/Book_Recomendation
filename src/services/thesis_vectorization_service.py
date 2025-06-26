

import socket


import aiohttp
from src.database.chroma_database.template_method import ThesisProcessor
from src.database.postgres_database.thesis.process_status_repository import ProcessStatusRepository
from src.database.postgres_database.thesis.thesis_repository import ThesisRepository
from src.database.postgres_database.thesis.init_db import AsyncSessionLocal


from src.models.thesis_model import ProcessName, ProcessStatus
from src.schemas.thesis_schema import ThesisSchema


class TesisError(Exception): pass
class CriticalProcessError(Exception): pass

class ThesisVectorizationService:
    def __init__(self, thesis_repository: ThesisRepository, process_status_repository: ProcessStatusRepository):
        self.thesis_repository = thesis_repository
        self.process_status_repository = process_status_repository


    async def vectorize_theses(self):
        success, errors = 0, []
        try:
            await self._set_process_status(ProcessStatus.RUNNING)
            theses = await self._get_non_vectorized_theses()
            

            for thesis in theses:
                try:
                    await self._vectorize_thesis(thesis)
                    success += 1
                except TesisError as e:
                    errors.append(f"Tesis {thesis.handle}: {e}")
                except Exception as e:
                    # Errores críticos de red o conexión
                    if isinstance(e, (aiohttp.ClientError, ConnectionError, socket.timeout, TimeoutError)):
                        raise CriticalProcessError(f"Error de conexión {thesis.handle}: {e}")
                    errors.append(f"Tesis {thesis.handle}: {e}")

            await self._set_process_status(ProcessStatus.COMPLETED, errors)
        except Exception as e:
            errors.append(str(e))
            await self._set_process_status(ProcessStatus.FAILED, errors)
        finally:
            print(f"Vectorización completa. Éxito: {success}, Errores: {len(errors)}")

    async def _vectorize_thesis(self, thesis_schema: ThesisSchema):
        # Crear una copia de los metadatos originales para no modificarlos directamente
        processed_metadata = thesis_schema.metadata_json.copy() if thesis_schema.metadata_json else {}
        
        # Agregar el handle como metadato adicional
        processed_metadata['handle'] = thesis_schema.handle
        
        processor = ThesisProcessor(
            path_or_url=thesis_schema.download_url,
            metadata=processed_metadata  # Usar los metadatos actualizados
        )
        
        await processor.process_and_store()

       
        async with AsyncSessionLocal() as session:
            await self.thesis_repository.mark_as_vectorized(session, thesis_schema.handle)

    async def _set_process_status(self, status, errors=None):
        async with AsyncSessionLocal() as session:
            await self.process_status_repository.set_status(
                session,
                process_name=ProcessName.VECTORIZE_THESIS,
                status=status,
                error_messages=errors or []
            )

    async def _get_non_vectorized_theses(self):
        async with AsyncSessionLocal() as session:
            raw_theses = await self.thesis_repository.get_non_vectorized_theses(session)
            return [ThesisSchema(**vars(th)) for th in raw_theses]
        
    async def get_vectorization_status(self) -> dict:
        async with AsyncSessionLocal() as session:
            status = await self.process_status_repository.get_status(session, ProcessName.VECTORIZE_THESIS)
            return status or {}