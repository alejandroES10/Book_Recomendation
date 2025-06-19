



# import asyncio
# import requests
# from src.interfaces.ithesis_data_importer_service import IThesisDataImporterService
# from src.services.dspace_service import DSpaceService
# from src.database.postgres_database.thesis.thesis_repository import ThesisRepository
# from src.database.postgres_database.thesis.init_db import AsyncSessionLocal
# from src.schemas.thesis_schema import ThesisSchema

# COMMUNITY_NAME = "Tesis de Diploma, Maestrías y Doctorados"


# from src.database.postgres_database.thesis.process_status_repository import ProcessStatusRepository
# from src.models.thesis_model import ProcessName, ProcessStatus

# class CreateUrl():
#     @staticmethod
#     def create_url_repository_https(bitstream)-> str:
#      return f"https://repositorio.cujae.edu.cu/server/api/core/bitstreams/{bitstream.uuid}/content"
    
#     @staticmethod
#     def create_url_repository_http(item,bitstream)-> str:
#        return f"http://tesis.cujae.edu.cu/bitstream/handle/{item.handle}/{bitstream.name}?sequence=1&isAllowed=y"

# class ThesisDataImporterService(IThesisDataImporterService):

#     def __init__(
#         self,
#         dspace_service: DSpaceService,
#         thesis_repository: ThesisRepository,
#         process_status_repository: ProcessStatusRepository
#     ):
#         self.dspace_service = dspace_service
#         self.thesis_repository = thesis_repository
#         self.process_status_repository = process_status_repository

#     async def upsert_theses(self):
#         process_name = ProcessName.IMPORT_THESIS

#         async with AsyncSessionLocal() as session:
#             try:
#                 await self.process_status_repository.set_status(session, process_name, ProcessStatus.RUNNING)

#                 items = await self.dspace_service.get_items_by_top_community_name(COMMUNITY_NAME, limit=20)

#                 if not items:
#                     await self.process_status_repository.set_status(session, process_name, ProcessStatus.COMPLETED)
#                     print("[INFO] No se encontraron ítems en la comunidad.")
#                     return

#                 handles_en_bd = {
#                     thesis.handle
#                     for thesis in await self.thesis_repository.get_all(session)
#                 }

#                 nuevas_tesis = []
#                 actualizadas = 0
#                 ya_procesadas = 0

#                 for item in items:
#                     bundles = await self.dspace_service.get_bundles_by_item(item)
#                     if not bundles:
#                         continue

#                     original_bundle = next((b for b in bundles if getattr(b, "name", "").upper() == "ORIGINAL"), None)
#                     if not original_bundle:
#                         continue

#                     bitstreams = await self.dspace_service.get_bitstreams_by_bundle(original_bundle)
#                     if not bitstreams or not isinstance(bitstreams, list):
#                         continue

#                     bitstream = bitstreams[0]
#                     pdf_url = CreateUrl.create_url_repository_https(bitstream)
#                     cleaned_metadata = self._clean_metadata(item.metadata)
#                     thesis_schema = self._build_thesis_schema(item, bitstream, pdf_url, cleaned_metadata)

#                     # Si no existe el handle, preparar para inserción en bloque
#                     if thesis_schema.handle not in handles_en_bd:
#                         nuevas_tesis.append(thesis_schema)
#                     else:
#                         # Si ya existe, pero URL cambió y aún no se ha vectorizado
#                         existing = await self.thesis_repository.get_by_handle(session, thesis_schema.handle)
#                         if existing and not existing.is_vectorized and existing.download_url != thesis_schema.download_url:
#                             existing.download_url = thesis_schema.download_url
#                             existing.is_vectorized = False
#                             await session.commit()
#                             actualizadas += 1
#                         elif existing and existing.is_vectorized:
#                             ya_procesadas += 1

#                 # Inserción masiva
#                 if nuevas_tesis:
#                     await self.thesis_repository.bulk_insert_theses(session, nuevas_tesis)

#                 print(f"[INFO] Total nuevas: {len(nuevas_tesis)}, actualizadas: {actualizadas}, ya vectorizadas: {ya_procesadas}")
#                 await self.process_status_repository.set_status(session, process_name, ProcessStatus.COMPLETED)

#             except Exception as e:
#                 await self.process_status_repository.set_status(session, process_name, ProcessStatus.FAILED, error_messages=[str(e)])
#                 print(f"[ERROR] Proceso de importación fallido: {e}")
#                 raise

#     def _clean_metadata(self, metadata: dict) -> dict:
#         """
#         Cleans and transforms the metadata, returning only relevant keys and values.
#         """
#         exclude_keys = {
#             "dc.language.iso",
#             "dc.location.physical",
#             "dc.provenance",
#             "dc.publisher",
#             "dc.subject",
#             "dc.contributor.tutor",
#             "dc.date.accessioned",
#             "dc.date.available",
#             "dc.date.issued",
#             "dc.description",
#             "dc.description.abstract",
#             "dc.type"
#         }

#         cleaned = {}

#         for key, entries in metadata.items():
#             if key in exclude_keys:
#                 continue
#             values = [entry["value"] for entry in entries if "value" in entry]
#             cleaned[key] = values if len(values) > 1 else values[0]

#         return cleaned

#     def _build_thesis_schema(self, item, bitstream, pdf_url: str, cleaned_metadata: dict) -> ThesisSchema:


#         return ThesisSchema(
#             handle=item.handle,
#             metadata_json=cleaned_metadata,
#             original_name_document=bitstream.name,
#             size_bytes_document=bitstream.sizeBytes,
#             download_url=pdf_url,
#             is_vectorized=False
#         )
    
#     async def _process_item(self, item) -> bool:
#         bundles = await self.dspace_service.get_bundles_by_item(item)
#         if not bundles:
#             return False

#         original_bundle = next((b for b in bundles if getattr(b, "name", "").upper() == "ORIGINAL"), None)
#         if not original_bundle:
#             return False

#         bitstreams = await self.dspace_service.get_bitstreams_by_bundle(original_bundle)
#         if not bitstreams or not isinstance(bitstreams, list):
#             return False
        

#         bitstream = bitstreams[0]
#         print("uuid Bitstream en 0:")
#         print(bitstream.uuid)

#         #factory
#         pdf_url = CreateUrl.create_url_repository_https(bitstream)

#         # pdf_url = f"http://tesis.cujae.edu.cu/bitstream/handle/{item.handle}/{bitstream.name}?sequence=1&isAllowed=y"

#         async with AsyncSessionLocal() as session:
#             cleaned_metadata = self._clean_metadata(item.metadata)
#             thesis_schema = self._build_thesis_schema(item, bitstream, pdf_url, cleaned_metadata)
#             await self.thesis_repository.upsert_thesis(session, thesis_schema)

#         return True
    
#     async def get_import_status(self) -> dict:
#         async with AsyncSessionLocal() as session:
#             status = await self.process_status_repository.get_status(session, ProcessName.IMPORT_THESIS)
#             return status or {}


import asyncio
import requests
from src.interfaces.ithesis_data_importer_service import IThesisDataImporterService
from src.services.dspace_service import DSpaceService
from src.database.postgres_database.thesis.thesis_repository import ThesisRepository
from src.database.postgres_database.thesis.init_db import AsyncSessionLocal
from src.schemas.thesis_schema import ThesisSchema
from src.database.postgres_database.thesis.process_status_repository import ProcessStatusRepository
from src.models.thesis_model import ProcessName, ProcessStatus

TOP_COMMUNITY_NAME = "Tesis de Diploma, Maestrías y Doctorados"

class UrlFactory:
    @staticmethod
    def create_https_repository_url(bitstream) -> str:
        return f"https://repositorio.cujae.edu.cu/server/api/core/bitstreams/{bitstream.uuid}/content"

    @staticmethod
    def create_http_repository_url(item, bitstream) -> str:
        return f"http://tesis.cujae.edu.cu/bitstream/handle/{item.handle}/{bitstream.name}?sequence=1&isAllowed=y"

class ThesisDataImporterService(IThesisDataImporterService):
    def __init__(
        self,
        dspace_service: DSpaceService,
        thesis_repository: ThesisRepository,
        process_status_repository: ProcessStatusRepository
    ):
        self.dspace_service = dspace_service
        self.thesis_repository = thesis_repository
        self.process_status_repository = process_status_repository

    async def upsert_theses(self):
        process_name = ProcessName.IMPORT_THESIS

        async with AsyncSessionLocal() as session:
            try:
                await self.process_status_repository.set_status(session, process_name, ProcessStatus.RUNNING)

                items = await self.dspace_service.get_items_by_top_community_name(TOP_COMMUNITY_NAME, limit= 1000)
                print("HOLAAAAAAA")
                if not items:
                    await self.process_status_repository.set_status(session, process_name, ProcessStatus.COMPLETED)
                    print("[INFO] No se encontraron ítems en la comunidad.")
                    return

                handles_in_db = {
                    thesis.handle
                    for thesis in await self.thesis_repository.get_all(session)
                }

                new_theses = []
                updated_count = 0
                already_vectorized = 0

                for item in items:
                    bundles = await self.dspace_service.get_bundles_by_item(item)
                    if not bundles:
                        continue

                    original_bundle = next((b for b in bundles if getattr(b, "name", "").upper() == "ORIGINAL"), None)
                    if not original_bundle:
                        continue

                    bitstreams = await self.dspace_service.get_bitstreams_by_bundle(original_bundle)
                    if not bitstreams or not isinstance(bitstreams, list):
                        continue

                    bitstream = bitstreams[0]
                    pdf_url = UrlFactory.create_https_repository_url(bitstream)
                    cleaned_metadata = self._clean_metadata(item.metadata)
                    thesis_schema = self._build_thesis_schema(item, bitstream, pdf_url, cleaned_metadata)

                    if thesis_schema.handle not in handles_in_db:
                        new_theses.append(thesis_schema)
                    else:
                        existing = await self.thesis_repository.get_by_handle(session, thesis_schema.handle)
                        if existing and not existing.is_vectorized and existing.download_url != thesis_schema.download_url:
                            existing.download_url = thesis_schema.download_url
                            existing.is_vectorized = False
                            await session.commit()
                            updated_count += 1
                        elif existing and existing.is_vectorized:
                            already_vectorized += 1

                if new_theses:
                    await self.thesis_repository.bulk_insert_theses(session, new_theses)

                print(f"[INFO] Total nuevas: {len(new_theses)}, actualizadas: {updated_count}, ya vectorizadas: {already_vectorized}")
                await self.process_status_repository.set_status(session, process_name, ProcessStatus.COMPLETED)

            except Exception as e:
                await self.process_status_repository.set_status(session, process_name, ProcessStatus.FAILED, error_messages=[str(e)])
                print(f"[ERROR] Proceso de importación fallido: {e}")
                raise

    def _clean_metadata(self, metadata: dict) -> dict:
        exclude_keys = {
            "dc.language.iso",
            "dc.location.physical",
            "dc.provenance",
            "dc.publisher",
            "dc.subject",
            "dc.contributor.tutor",
            "dc.date.accessioned",
            "dc.date.available",
            "dc.date.issued",
            "dc.description",
            "dc.description.abstract",
            "dc.type"
        }

        cleaned = {}

        for key, entries in metadata.items():
            if key in exclude_keys:
                continue
            values = [entry["value"] for entry in entries if "value" in entry]
            cleaned[key] = values if len(values) > 1 else values[0]

        return cleaned

    def _build_thesis_schema(self, item, bitstream, pdf_url: str, cleaned_metadata: dict) -> ThesisSchema:
        return ThesisSchema(
            handle=item.handle,
            metadata_json=cleaned_metadata,
            original_name_document=bitstream.name,
            size_bytes_document=bitstream.sizeBytes,
            download_url=pdf_url,
            is_vectorized=False
        )

    async def _process_item(self, item) -> bool:
        bundles = await self.dspace_service.get_bundles_by_item(item)
        if not bundles:
            return False

        original_bundle = next((b for b in bundles if getattr(b, "name", "").upper() == "ORIGINAL"), None)
        if not original_bundle:
            return False

        bitstreams = await self.dspace_service.get_bitstreams_by_bundle(original_bundle)
        if not bitstreams or not isinstance(bitstreams, list):
            return False

        bitstream = bitstreams[0]
        print("uuid del Bitstream:")
        print(bitstream.uuid)

        pdf_url = UrlFactory.create_https_repository_url(bitstream)

        async with AsyncSessionLocal() as session:
            cleaned_metadata = self._clean_metadata(item.metadata)
            thesis_schema = self._build_thesis_schema(item, bitstream, pdf_url, cleaned_metadata)
            await self.thesis_repository.upsert_thesis(session, thesis_schema)

        return True

    async def get_import_status(self) -> dict:
        async with AsyncSessionLocal() as session:
            status = await self.process_status_repository.get_status(session, ProcessName.IMPORT_THESIS)
            return status or {}

# async def main():
#     dspace_service = DSpaceService("https://repositorio.cujae.edu.cu/server/api")
#     thesis_repository = ThesisRepository()
#     thesis_manager = ThesisDataImporterService(dspace_service, thesis_repository)

#     await thesis_manager.upsert_theses()

# if __name__ == "__main__":
#     asyncio.run(main())
