
from fastapi import APIRouter, File, HTTPException, UploadFile,Depends

from src.services.general_information_service import GeneralInformationService

from src.security.auth import validate_api_key

router = APIRouter()



general_info_service = GeneralInformationService()

@router.post("/", status_code=201,dependencies=[Depends(validate_api_key)])
async def create_documents_from_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    
    try:
       
       return await general_info_service.add_general_info(file)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
   


@router.delete("/{file_id}",dependencies=[Depends(validate_api_key)])
async def delete_document_by_file_id(file_id: str):
    try:
        await general_info_service.delete_general_info(file_id)
        return {"message": "Documents deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{id}",dependencies=[Depends(validate_api_key)])
async def get_document(id: str):
    try:
        document = await general_info_service.get_general_info_by_document_id(id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        return document
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/")
async def get_documents():
    try:
        return await general_info_service.get_all_general_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


# class GeneralInformationController:
#     def __init__(self):
#         self.router = APIRouter()
#         self.service = GeneralInformationService()

        
#         self._add_routes()

#     def _add_routes(self):
#         self.router.post("/", status_code=201, dependencies=[Depends(validate_api_key)])(self.create_document)
#         self.router.delete("/{file_id}", dependencies=[Depends(validate_api_key)])(self.delete_document)
#         self.router.get("/{id}", dependencies=[Depends(validate_api_key)])(self.get_document)
#         self.router.get("/", dependencies=[Depends(validate_api_key)])(self.get_all_documents)

#     async def create_document(self, file: UploadFile = File(...)):
#         if not file.filename.lower().endswith(".pdf"):
#             raise HTTPException(status_code=400, detail="Only PDF files are accepted")
#         try:
#             return await self.service.add_general_info(file)
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

#     async def delete_document(self, file_id: str):
#         try:
#             await self.service.delete_general_info(file_id)
#             return {"message": "Documents deleted successfully"}
#         except ValueError as e:
#             raise HTTPException(status_code=404, detail=str(e))
#         except Exception:
#             raise HTTPException(status_code=500, detail="Internal server error")

#     async def get_document(self, id: str):
#         try:
#             doc = await self.service.get_general_info_by_document_id(id)
#             if not doc:
#                 raise HTTPException(status_code=404, detail="Document not found")
#             return doc
#         except Exception:
#             raise HTTPException(status_code=500, detail="Internal server error")

#     async def get_all_documents(self):
#         try:
#             return await self.service.get_all_general_info()
#         except Exception:
#             raise HTTPException(status_code=500, detail="Internal server error")