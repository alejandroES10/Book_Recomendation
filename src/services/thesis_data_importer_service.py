



import asyncio
import requests
from src.interfaces.ithesis_data_importer_service import IThesisDataImporterService
from src.services.dspace_service import DSpaceService
from src.database.postgres.thesis.thesis_repository import ThesisRepository
from src.database.postgres.thesis.init_db import AsyncSessionLocal
from src.schemas.thesis_schema import ThesisSchema

COMMUNITY_NAME = "Tesis de Diploma, Maestrías y Doctorados"

class ThesisDataImporterService(IThesisDataImporterService):

    def __init__(self, dspace_service: DSpaceService, thesis_repository: ThesisRepository):
        self.dspace_service = dspace_service
        self.thesis_repository = thesis_repository

    # async def upsert_theses(self):
    #     """
    #     Inserts or updates theses in the database.
    #     """
    #     try:
    #         items = await self.dspace_service.get_items_by_top_community_name(COMMUNITY_NAME, limit=100)
    #     except Exception as e:
    #         print(f"[ERROR] Failed to fetch items: {e}")
    #         return

    #     if not items:
    #         print("[INFO] No items found in the community.")
    #         return

    #     for item in items:
    #         try:
    #             bundles = await self.dspace_service.get_bundles_by_item(item)
    #             if not bundles:
    #                 continue

    #             # Find the bundle named "ORIGINAL"
    #             original_bundle = next((b for b in bundles if getattr(b, "name", "").upper() == "ORIGINAL"), None)
    #             if not original_bundle:
    #                 continue

    #             bitstreams = await self.dspace_service.get_bitstreams_by_bundle(original_bundle)
    #             if not bitstreams or not isinstance(bitstreams, list):
    #                 continue

    #             bitstream = bitstreams[0]
    #             bitstream_uuid = bitstream.uuid 
    #             pdf_url = f"https://repositorio.cujae.edu.cu/server/api/core/bitstreams/{bitstream_uuid}/content"
                
    #             if not pdf_url:
    #                 continue
                
    #             async with AsyncSessionLocal() as session:
    #                 cleaned_metadata = self._clean_metadata(item.metadata)
    #                 thesis_schema = self._build_thesis_schema(item, bitstream, pdf_url, cleaned_metadata)
    #                 await self.thesis_repository.upsert_thesis(session,thesis_schema)

    #         except Exception as e:
    #             print(f"[ERROR] Error processing item '{getattr(item, 'handle', 'unknown')}': {e}")    
    # 
    
    async def upsert_theses(self):
        """
        Inserta o actualiza las tesis en la base de datos.
        Si se pierde la conexión a DSpace, se detiene el proceso.
        """
        try:
            items = await self.dspace_service.get_items_by_top_community_name(COMMUNITY_NAME, limit=100)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            print(f"[ERROR] Conexión fallida al obtener los ítems desde DSpace: {e}")
            raise  # Detiene completamente el proceso
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Fallo general en la petición a DSpace: {e}")
            raise
        except Exception as e:
            print(f"[ERROR] Otro error inesperado al obtener ítems: {e}")
            raise

        if not items:
            print("[INFO] No se encontraron ítems en la comunidad.")
            raise

        for item in items:
            try:
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
                bitstream_uuid = bitstream.uuid 
                pdf_url = f"https://repositorio.cujae.edu.cu/server/api/core/bitstreams/{bitstream_uuid}/content"
                
                if not pdf_url:
                    continue

                async with AsyncSessionLocal() as session:
                    cleaned_metadata = self._clean_metadata(item.metadata)
                    thesis_schema = self._build_thesis_schema(item, bitstream, pdf_url, cleaned_metadata)
                    await self.thesis_repository.upsert_thesis(session, thesis_schema)

            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                print(f"[ERROR] Conexión perdida al procesar el ítem '{getattr(item, 'handle', 'unknown')}': {e}")
                raise  # Detiene el proceso completamente
            except requests.exceptions.RequestException as e:
                print(f"[ERROR] Error de red general procesando el ítem '{getattr(item, 'handle', 'unknown')}': {e}")
                raise
            except Exception as e:
                print(f"[ERROR] Error procesando el ítem '{getattr(item, 'handle', 'unknown')}': {e}") 
                raise    

    def _clean_metadata(self, metadata: dict) -> dict:
        """
        Cleans and transforms the metadata, returning only relevant keys and values.
        """
        exclude_keys = {"dc.description.abstract"}
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
    
# async def main():
#     dspace_service = DSpaceService("https://repositorio.cujae.edu.cu/server/api")
#     thesis_repository = ThesisRepository()
#     thesis_manager = ThesisDataImporterService(dspace_service, thesis_repository)

#     await thesis_manager.upsert_theses()

# if __name__ == "__main__":
#     asyncio.run(main())
