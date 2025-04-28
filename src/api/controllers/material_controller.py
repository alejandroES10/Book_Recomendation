from fastapi import APIRouter, HTTPException,Depends
from langchain_core.documents import Document
from typing import List
from src.api.models.document_model import DocumentModel
from src.api.services.chromadb_service import ChromaDBService
from src.database.vector_store import collection_of_books
from src.api.security.auth import validate_api_key

router = APIRouter()

chroma_service = ChromaDBService(vector_store=collection_of_books)


# @router.post("/", status_code=201,dependencies=[Depends(validate_api_key)])
# async def create_documents(documents: List[DocumentModel]):
#     try:
#         document_objects = [
#             Document(
#                 page_content=doc.page_content,
#                 metadata = doc.metadata,
#                 id=str(doc.id))
#             for doc in documents
#         ]
#         ids = [str(doc.id) for doc in documents]
#         await chroma_service.add_documents_with_ids(document_objects, ids)
#         return {"message": "Documents created successfully"}
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/", status_code=201, dependencies=[Depends(validate_api_key)])
async def create_documents(documents: List[DocumentModel]):
    try:
        await chroma_service.add_documents_with_ids(documents)
        return {"message": "Documents created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")



@router.delete("/{id}",dependencies=[Depends(validate_api_key)])
async def delete_document(id: str):
    try:
        await chroma_service.delete_document_by_id(id)
        return {"message": "Document deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


# @router.put("/",dependencies=[Depends(validate_api_key)])
# async def update_documents(documents: List[DocumentModel]):
#     try:
#         ids = [doc.id for doc in documents]
#         await chroma_service.update_documents(ids=ids, documents=documents)
#         return {"message": "Documents updated successfully"}
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/", dependencies=[Depends(validate_api_key)])
async def update_documents(documents: List[DocumentModel]):
    try:
        await chroma_service.update_documents(documents)
        return {"message": "Documents updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{id}")
async def get_document(id: str):
    try:
        document = await chroma_service.find_one(id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        return document
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/")
async def get_documents():
    try:
        return await chroma_service.find_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")