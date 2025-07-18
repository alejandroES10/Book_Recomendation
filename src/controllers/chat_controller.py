

from fastapi import APIRouter, HTTPException, Depends
from src.schemas.chat_request_schema import ChatRequestSchema
from src.interfaces.ichat_service import IChatService
from src.security.auth import validate_api_key

class ChatController:
    def __init__(self, chat_service: IChatService):
        self.router = APIRouter()
        self.chat_service = chat_service
        self._add_routes()

    def _add_routes(self):
        self.router.post("/", dependencies=[Depends(validate_api_key)])(self.chat)
        self.router.get("/{session_id}")(self.get_chat_history)
        self.router.delete("/{session_id}", dependencies=[Depends(validate_api_key)])(self.delete_chat_history)

    async def chat(self, request: ChatRequestSchema):
        try:
            return await self.chat_service.get_chat_bot_answer(request.session_id, request.input)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")

    async def get_chat_history(self, session_id: str):
        try:
            return await self.chat_service.get_chat_history(session_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")

    async def delete_chat_history(self, session_id: str):
        try:
            await self.chat_service.delete_chat_history(session_id)
            return {"message": "Historial de chat eliminado correctamente"}
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")
