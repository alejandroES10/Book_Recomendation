# src/controllers/thesis_import_controller.py

from fastapi import APIRouter, HTTPException, Depends
from src.security.auth import validate_api_key
from src.interfaces.ithesis_data_importer_service import IThesisDataImporterService

class ThesisImportController:
    def __init__(self, thesis_import_service: IThesisDataImporterService):
        self.router = APIRouter()
        self.thesis_import_service = thesis_import_service
        self._add_routes()

    def _add_routes(self):
        self.router.post("/", status_code=202, dependencies=[Depends(validate_api_key)])(self.import_theses)

    async def import_theses(self):
        try:
            await self.thesis_import_service.upsert_theses()
            return {"message": "Thesis import initiated successfully."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")
