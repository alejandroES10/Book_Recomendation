# src/controllers/thesis_import_controller.py

from fastapi import APIRouter, HTTPException, Depends
import requests
from src.security.auth import validate_api_key
from src.interfaces.ithesis_data_importer_service import IThesisDataImporterService

class ThesisImportController:
    def __init__(self, thesis_import_service: IThesisDataImporterService):
        self.router = APIRouter()
        self.thesis_import_service = thesis_import_service
        self._add_routes()

    def _add_routes(self):
        self.router.post("/", status_code=200, dependencies=[Depends(validate_api_key)])(self.import_theses)

    # async def import_theses(self):
    #     try:
    #         await self.thesis_import_service.upsert_theses()
    #         # return {"message": "Tthesis import process carried out."}
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")

    async def import_theses(self):
            try:
                await self.thesis_import_service.upsert_theses()
                return {"message": "Thesis import process completed successfully."}
            except requests.exceptions.ConnectionError:
                raise HTTPException(
                    status_code=503,
                    detail="No se pudo conectar al servidor de DSpace. Verifique la conexión de red."
                )
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Thesis import failed: {str(e)}"
                )