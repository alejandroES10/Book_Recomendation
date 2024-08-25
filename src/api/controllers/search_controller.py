# api/controllers/search_controller.py

from fastapi import APIRouter
from api.services.search_services import SearchService

router = APIRouter()



@router.get("/{contentToSearch}")
async def search_results(contentToSearch: str):
    return SearchService.get_results(contentToSearch)
