from pydantic import BaseModel, field_validator
from typing import Annotated

MAX_WORDS = 1000  # Aproximadamente 8000 tokens

class ChatRequestModel(BaseModel):
    session_id: str
    input: str

    @field_validator("input")
    @classmethod
    def validate_input_length(cls, v: str):
        if len(v.split()) > MAX_WORDS:
            raise ValueError(f"El texto supera el límite de {MAX_WORDS} palabras.")
        return v
