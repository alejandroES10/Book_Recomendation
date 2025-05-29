# from fastapi import APIRouter, HTTPException,Depends
# from langchain_core.documents import Document
# from typing import List
# from src.schemas.book_metadata_schema import BookMetadataSchema
# from src.services.book_metadata_service import BookMetadataService
# from src.services.chromadb_service import ChromaDBService

# from src.security.auth import validate_api_key

# router = APIRouter()



# book_metadata_service = BookMetadataService()

# @router.post("/", status_code=201, dependencies=[Depends(validate_api_key)])
# async def create_books(documents: List[BookMetadataSchema]):
#     try:
#         await book_metadata_service.add_books(documents)
#         return {"message": "Documents created successfully"}
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Internal server error")


# @router.delete("/{id}",dependencies=[Depends(validate_api_key)])
# async def delete_document(id: str):
#     try:
#         await book_metadata_service.delete_book(id)
#         return {"message": "Document deleted successfully"}
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Internal server error")


# @router.put("/", dependencies=[Depends(validate_api_key)])
# async def update_book(documents: List[BookMetadataSchema]):
#     try:
#         await book_metadata_service.update_book(documents)
#         return {"message": "Documents updated successfully"}
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Internal server error")


# @router.get("/{id}")
# async def get_book_metadata(id: str):
#     try:
#         document = await book_metadata_service.get_book(id)
#         if not document:
#             raise HTTPException(status_code=404, detail="Document not found")
#         return document
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Internal server error")


# @router.get("/")
# async def get_all_book_metadata():
#     try:
#         return await book_metadata_service.get_all_books()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Internal server error")



from fastapi import APIRouter, HTTPException, Depends
from typing import List
from src.schemas.book_metadata_schema import BookMetadataSchema
from src.security.auth import validate_api_key
from src.interfaces.ibook_metadata_service import IBookMetadataService

class BookMetadataController:
    def __init__(self, service: IBookMetadataService):
        self.router = APIRouter()
        self.book_metadata_service = service
        self._add_routes()

    def _add_routes(self):
        self.router.post("/", status_code=201, dependencies=[Depends(validate_api_key)])(self.create_book_metadata)
        self.router.delete("/{id}", dependencies=[Depends(validate_api_key)])(self.delete_book_metadata)
        self.router.put("/", dependencies=[Depends(validate_api_key)])(self.update_book_metadata)
        self.router.get("/{id}")(self.get_book_metadata)
        self.router.get("/")(self.get_all_book_metadata)

    async def create_book_metadata(self, documents: List[BookMetadataSchema]):
        try:
            await self.book_metadata_service.add_books(documents)
            return {"message": "Documents created successfully"}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")

    async def delete_book_metadata(self, id: str):
        try:
            await self.book_metadata_service.delete_book(id)
            return {"message": "Document deleted successfully"}
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")

    async def update_book_metadata(self, documents: List[BookMetadataSchema]):
        try:
            await self.book_metadata_service.update_book(documents)
            return {"message": "Documents updated successfully"}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")

    async def get_book_metadata(self, id: str):
        try:
            document = await self.book_metadata_service.get_book(id)
            # if not document:
            #     raise HTTPException(status_code=404, detail="Document not found")
            return document
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")

    async def get_all_book_metadata(self):
        try:
            return await self.book_metadata_service.get_all_books()
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")
