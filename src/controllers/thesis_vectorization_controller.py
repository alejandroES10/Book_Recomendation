# src/controllers/thesis_import_controller.py

from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends
from src.models.thesis_model import ProcessStatus
from src.security.auth import validate_api_key
from src.interfaces.ithesis_vectorization_service import IThesisVectorizationService

class ThesisVectorizationController:
    def __init__(self, thesis_vectorization_service: IThesisVectorizationService):
        self.router = APIRouter()
        self.thesis_vectorization_service = thesis_vectorization_service
        self._add_routes()

    def _add_routes(self):
        self.router.post("/start", status_code=202, dependencies=[Depends(validate_api_key)])(self.vectorize_theses)
        self.router.get("/status", dependencies=[Depends(validate_api_key)])(self.get_vectorization_status)

    async def vectorize_theses(self, background_tasks: BackgroundTasks):
        try:
            status = await self.thesis_vectorization_service.get_vectorization_status()
            if status and status.get("status") == ProcessStatus.RUNNING:
                raise HTTPException(
                    status_code=409,
                    detail="Thesis vectorization process is already running."
                )

            background_tasks.add_task(self.thesis_vectorization_service.vectorize_theses)
            return {"message": "Thesis vectorization process started."}
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to start thesis vectorization process: {str(e)}"
            )

    async def get_vectorization_status(self):
        try:
            status = await self.thesis_vectorization_service.get_vectorization_status()
            if not status:
                raise HTTPException(
                    status_code=404,
                    detail="No vectorization status found."
                )
            return status
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error retrieving vectorization status: {str(e)}"
            )