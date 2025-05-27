# src/controllers/thesis_import_controller.py

from fastapi import APIRouter, HTTPException, Depends
from src.security.auth import validate_api_key
from src.interfaces.ithesis_vectorization_service import IThesisVectorizationService

class ThesisVectorizationController:
    def __init__(self, thesis_vectorization_service: IThesisVectorizationService):
        self.router = APIRouter()
        self.thesis_vectorization_service = thesis_vectorization_service
        self._add_routes()

    def _add_routes(self):
        self.router.post("/", status_code=202, dependencies=[Depends(validate_api_key)])(self.import_theses)

    async def import_theses(self):
        try:
            await self.thesis_vectorization_service.vectorize_theses
            return {"message": "Thesis vectorization initiated successfully."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")
