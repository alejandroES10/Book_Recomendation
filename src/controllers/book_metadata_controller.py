

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from src.schemas.book_metadata_schema import BookCreateSchema, BookUpdateSchema, MetadataBaseSchema
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
        self.router.put("/{id}",dependencies=[Depends(validate_api_key)])(self.update_book_metadata)
        self.router.get("/{id}",dependencies=[Depends(validate_api_key)])(self.get_book_metadata)
        self.router.get("/",dependencies=[Depends(validate_api_key)])(self.get_all_book_metadata)

    async def create_book_metadata(self, books: List[BookCreateSchema]):
        try:
            await self.book_metadata_service.add_books(books)
            return {"message": "Metadatos de libros creados correctamente"}
        except ValueError as e:
            raise HTTPException(status_code=409, detail=str(e))
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")

    async def delete_book_metadata(self, id: str):
        try:
            await self.book_metadata_service.delete_book(id)
            return {"message": "Metadatos de libro eliminados correctamente"}
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")

    async def update_book_metadata(self,id:str, book_metadata: BookUpdateSchema):
        try:
            book = BookCreateSchema(id=id, metadata=book_metadata.metadata)
            await self.book_metadata_service.update_book(book)
            return {"message": "Metadatos de libro actualizados correctamente"}
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
