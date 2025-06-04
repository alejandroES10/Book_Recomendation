
import asyncio
from typing import List
from src.database.chroma_database.template_method import ThesisProcessor
from src.database.chroma_database.thesis_collection import ThesisCollection
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
                    raise CriticalProcessError(f"Error crítico en {thesis.handle}: {e}")

            await self._set_process_status(ProcessStatus.COMPLETED, errors)
        except Exception as e:
            errors.append(str(e))
            await self._set_process_status(ProcessStatus.FAILED, errors)
        finally:
            print(f"Vectorización completa. Éxito: {success}, Errores: {len(errors)}")

    async def _vectorize_thesis(self, thesis_schema):
        processor = ThesisProcessor(
            path_or_url=thesis_schema.download_url,
            metadata=thesis_schema.metadata_json
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