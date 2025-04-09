from fastapi import APIRouter, HTTPException,Depends
from src.api.services.chat_service import ChatService
from src.api.models.chat_request_model import ChatRequestModel
from src.api.security.auth import validate_api_key

router = APIRouter()


@router.post("/",dependencies=[Depends(validate_api_key)])
async def chat(request: ChatRequestModel):
    try:
        return await ChatService.get_chat_bot_answer(request.session_id, request.input)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{session_id}")
async def get_chat_history(session_id: str):
    try:
        history = await ChatService.get_chat_history(session_id)
        return {"history": history}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{session_id}")
async def delete_chat_history(session_id: str):
    try:
        await ChatService.delete_chat_history(session_id)
        return {"message": "Chat history deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")