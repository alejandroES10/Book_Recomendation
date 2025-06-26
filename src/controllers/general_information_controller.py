
import re
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from pydantic import BaseModel, Field
from src.security.auth import validate_api_key
from src.interfaces.igeneral_information_service import IGeneralInformationService

class GeneralInfoDocumentSchema(BaseModel):
    file_id: str = Field(
        ...,
        min_length=1,
        pattern=r'^\S+$',
        description="File ID no puede tener espacios y debe tener al menos 1 carácter"
    )
    file: UploadFile = File(...)


class GeneralInformationController:
    def __init__(self, service: IGeneralInformationService):
        self.router = APIRouter()
        self.general_info_service = service
        self._add_routes()

    def _add_routes(self):
        self.router.post("/", status_code=201, dependencies=[Depends(validate_api_key)])(self.create_documents_from_pdf)
        self.router.delete("/{file_id}", dependencies=[Depends(validate_api_key)])(self.delete_document_by_file_id)
        self.router.get("/{file_id}", dependencies=[Depends(validate_api_key)])(self.get_document)
        self.router.get("/",dependencies=[Depends(validate_api_key)])(self.get_documents)

   
    async def create_documents_from_pdf(self, 
                                        file:Annotated[UploadFile,File()],
                                        file_id:Annotated[str,Form()]):
        if not file_id or not file_id.strip():
            raise HTTPException(status_code=422, detail="file_id no puede estar vacío")
        
        if re.search(r'\s', file_id):
            raise HTTPException(
                status_code=422,
                detail="El file_id no puede contener espacios en blanco"
            )
        extension = file.filename.lower().split('.')[-1]
        if extension not in ['pdf', 'docx']:
            raise HTTPException(status_code=422, detail="Solo se aceptan archivos PDF o DOCX")

        try:
            return await self.general_info_service.add_general_info(file_id,file)
        except ValueError as e:
            raise HTTPException(status_code=409, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error procesando el documento: {str(e)}")


    async def delete_document_by_file_id(self, file_id: str):
        try:
            await self.general_info_service.delete_general_info_by_file_id(file_id)
            return {"message": "Información general eliminada correctamente"}
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")

    async def get_document(self, file_id: str):
        try:
            document = await self.general_info_service.get_general_info_by_file_id(file_id)
            return document
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")

    async def get_documents(self):
        try:
            return await self.general_info_service.get_all_general_info()
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")
