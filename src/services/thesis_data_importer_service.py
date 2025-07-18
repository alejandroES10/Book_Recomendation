



import traceback
from src.interfaces.ithesis_data_importer_service import IThesisDataImporterService
from src.services.dspace_service import DSpaceService
from src.database.postgres_database.thesis.thesis_repository import ThesisRepository
from src.database.postgres_database.thesis.init_db import AsyncSessionLocal
from src.schemas.thesis_schema import ThesisSchema

COMMUNITY_NAME = "Tesis de Diploma, Maestrías y Doctorados"


from src.database.postgres_database.thesis.process_status_repository import ProcessStatusRepository
from src.models.thesis_model import ProcessName, ProcessStatus

class CreateUrl():
    @staticmethod
    def create_url_repository_https(bitstream)-> str:
     return f"https://repositorio.cujae.edu.cu/server/api/core/bitstreams/{bitstream.uuid}/content"
    
    @staticmethod
    def create_url_repository_http(item,bitstream)-> str:
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

                #Para de desarrollo y pruebas se pasa limit = un valor para que traiga esa cantidad de ítems
                #Para producción no hay que pasar parámetro limit, ya que se traen todos los ítems de la comunidad
                items = await self.dspace_service.get_items_by_top_community_name(COMMUNITY_NAME, limit=20)
                print(f"[INFO] Cantidad de ítems encontrados: {len(items)}")

                if not items:
                    await self.process_status_repository.set_status(session, process_name, ProcessStatus.COMPLETED)
                    print("[INFO] No se encontraron ítems en la comunidad.")
                    return

                processed_count = 0
                for item in items:
                    try:
                        if not await self._process_item(item):
                            continue
                        processed_count += 1
                    except Exception as e:
                        handle = getattr(item, 'handle', 'unknown')
                        raise RuntimeError(f"[ERROR] Fallo procesando ítem '{handle}': {e}")

                print(f"[INFO] Total de tesis procesadas: {processed_count}")
                await self.process_status_repository.set_status(session, process_name, ProcessStatus.COMPLETED)

            except Exception as e:
                
                error_message = repr(e) or "Error sin mensaje"
                print(f"[ERROR] Proceso de importación fallido: {traceback.format_exc()}")
                await self.process_status_repository.set_status(
                    session,
                    process_name,
                    ProcessStatus.FAILED,
                    error_messages=[error_message]
                )
                raise


    async def get_import_status(self) -> dict:
        async with AsyncSessionLocal() as session:
            status = await self.process_status_repository.get_status(session, ProcessName.IMPORT_THESIS)
            return status or {}


    def _clean_metadata(self, metadata: dict) -> dict:
        """
        Cleans and transforms the metadata, returning only relevant keys and values.
        """
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
        print("uuid Bitstream en 0:")
        print(bitstream.uuid)

       
        pdf_url = CreateUrl.create_url_repository_https(bitstream)


        async with AsyncSessionLocal() as session:
            cleaned_metadata = self._clean_metadata(item.metadata)
            thesis_schema = self._build_thesis_schema(item, bitstream, pdf_url, cleaned_metadata)
            await self.thesis_repository.upsert_thesis(session, thesis_schema)

        return True
    
# async def main():
#     dspace_service = DSpaceService("https://repositorio.cujae.edu.cu/server/api")
#     thesis_repository = ThesisRepository()
#     thesis_manager = ThesisDataImporterService(dspace_service, thesis_repository)

#     await thesis_manager.upsert_theses()

# if __name__ == "__main__":
#     asyncio.run(main())
