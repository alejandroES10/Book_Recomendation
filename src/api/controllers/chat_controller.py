from api.models.document_model import DocumentModel
from api.models.search_model import SearchModel
from fastapi import APIRouter, HTTPException, Query
from chatbot.agent import agent_executor

# from fastapi import APIRouter
from api.services.document_service import ChatService
from langchain_core.documents import Document
from typing import List,Optional
from langchain_core.messages import AIMessage, HumanMessage
router = APIRouter()


@router.get("/chat/")
async def search_results(session_id: str = Query(...), input: str = Query(...)):
    return ChatService.get_chat_bot_answer(session_id, input)