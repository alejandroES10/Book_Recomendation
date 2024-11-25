
from fastapi import APIRouter, HTTPException, Query


# from fastapi import APIRouter
from src.api.services.chat_service import ChatService
from langchain_core.documents import Document
from typing import List,Optional
from langchain_core.messages import AIMessage, HumanMessage
router = APIRouter()


@router.get("/")
async def search_results(session_id: str = Query(...), input: str = Query(...)):
    return ChatService.get_chat_bot_answer(session_id, input)