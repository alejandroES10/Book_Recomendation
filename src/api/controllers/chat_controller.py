
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

@router.get("/{id}")
async def get_chat_history(id):
    return ChatService.get_chat_history(id)

@router.delete("/{id}")
async def delete_chat(id: str):
    try:
        ChatService.delete_chat_history(id)
        response = {"message": "chat history deleted successfully"}
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))