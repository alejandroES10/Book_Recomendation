from pydantic import BaseModel

class ChatRequestModel(BaseModel):
    session_id: str
    input: str