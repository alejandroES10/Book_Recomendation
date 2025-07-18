# src/controllers/thesis_import_controller.py

from fastapi import APIRouter, HTTPException, Depends

from src.models.thesis_model import  ProcessStatus
from src.security.auth import validate_api_key
from src.interfaces.ithesis_data_importer_service import IThesisDataImporterService


from fastapi import APIRouter, HTTPException, Depends
from src.security.auth import validate_api_key
from src.interfaces.ithesis_data_importer_service import IThesisDataImporterService

from fastapi import BackgroundTasks



class ThesisImportController:
    def __init__(
        self,
        thesis_import_service: IThesisDataImporterService,
    ):
        self.router = APIRouter()
        self.thesis_import_service = thesis_import_service
        self._add_routes()

    def _add_routes(self):
        self.router.post("/start", status_code=202, dependencies=[Depends(validate_api_key)])(self.import_theses)
        self.router.get("/status", dependencies=[Depends(validate_api_key)])(self.get_import_status)

    async def import_theses(self, background_tasks: BackgroundTasks):
        try:
            status = await self.thesis_import_service.get_import_status()

            if status and status.get("status") == ProcessStatus.RUNNING:
                raise HTTPException(
                    status_code=409,
                    detail="No se puede iniciar porque el proceso de obtención de información de tesis ya está en estado RUNNING"
                )
            background_tasks.add_task(self.thesis_import_service.upsert_theses)
            return {"message": "Proceso de obtención de información de tesis iniciado"}
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Fallo al iniciar el proceso de obtención de información de tesis: {str(e)}"
            )

    async def get_import_status(self):
        try:
            status = await self.thesis_import_service.get_import_status()
            if not status:
                raise HTTPException(
                    status_code=404,
                    detail="No import status found."
                )
            return status
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error retrieving thesis import status: {str(e)}"
                )
