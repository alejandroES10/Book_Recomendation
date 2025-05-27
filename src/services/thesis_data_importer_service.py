



import asyncio
from src.interfaces.ithesis_data_importer_service import IThesisDataImporterService
from src.services.dspace_service import DSpaceService
from src.database.postgres.thesis.thesis_repository import ThesisRepository, AsyncSessionLocal
from src.schemas.thesis_schema import ThesisSchema

COMMUNITY_NAME = "Tesis de Diploma, Maestrías y Doctorados"

class ThesisDataImporterService(IThesisDataImporterService):

    def __init__(self, dspace_service: DSpaceService, thesis_repository: ThesisRepository):
        self.dspace_service = dspace_service
        self.thesis_repository = thesis_repository

    async def upsert_theses(self):
        """
        Inserts or updates theses in the database.
        """
        try:
            items = await self.dspace_service.get_items_by_top_community_name(COMMUNITY_NAME, limit=10)
        except Exception as e:
            print(f"[ERROR] Failed to fetch items: {e}")
            return

        if not items:
            print("[INFO] No items found in the community.")
            return

        for item in items:
            try:
                bundles = await self.dspace_service.get_bundles_by_item(item)
                if not bundles:
                    continue

                # Find the bundle named "ORIGINAL"
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
                    thesis_dto = self._build_thesis_dto(item, bitstream, pdf_url, cleaned_metadata)
                    await self.thesis_repository.upsert_thesis(session,thesis_dto)

            except Exception as e:
                print(f"[ERROR] Error processing item '{getattr(item, 'handle', 'unknown')}': {e}")         

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

    def _build_thesis_dto(self, item, bitstream, pdf_url: str, cleaned_metadata: dict) -> ThesisSchema:
        return ThesisSchema(
            handle=item.handle,
            metadata_json=cleaned_metadata,
            original_name=bitstream.name,
            size_bytes=bitstream.sizeBytes,
            download_url=pdf_url,
            checksum_md5="To be updated",
            is_processed=False
        )
    
async def main():
    dspace_service = DSpaceService("https://repositorio.cujae.edu.cu/server/api")
    thesis_repository = ThesisRepository()
    thesis_manager = ThesisDataImporterService(dspace_service, thesis_repository)

    await thesis_manager.upsert_theses()

if __name__ == "__main__":
    asyncio.run(main())
