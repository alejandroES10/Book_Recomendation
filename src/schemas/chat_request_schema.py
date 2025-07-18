from pydantic import BaseModel, field_validator
from typing import Annotated

# MAX_WORDS = 1000  # Aproximadamente 8000 tokens

# class ChatRequestSchema(BaseModel):
#     session_id: str
#     input: str

#     @field_validator("input")
#     @classmethod
#     def validate_input_length(cls, v: str):
#         if len(v.split()) > MAX_WORDS:
#             raise ValueError(f"El texto supera el límite de {MAX_WORDS} palabras.")
#         return v

from pydantic import BaseModel, Field, field_validator
from typing import Annotated

MAX_WORDS = 1000  # Aproximadamente 8000 tokens

# class ChatRequestSchema(BaseModel):
#     session_id: str = Field(..., min_length=1, description="ID de sesión no puede estar vacío")
#     input: str = Field(..., min_length=1, description="Texto de entrada no puede estar vacío")

#     @field_validator("session_id")
#     @classmethod
#     def validate_session_id(cls, v: str) -> str:
#         """Valida que el session_id no esté vacío y no contenga solo espacios"""
#         if not v.strip():
#             raise ValueError("El session_id no puede estar vacío o contener solo espacios")
#         return v.strip()

#     @field_validator("input")
#     @classmethod
#     def validate_input(cls, v: str) -> str:
#         """Valida que el input no esté vacío y cumpla con el límite de palabras"""
#         if not v.strip():
#             raise ValueError("El input no puede estar vacío o contener solo espacios")
        
#         words = v.split()
#         if len(words) > MAX_WORDS:
#             raise ValueError(f"El texto supera el límite de {MAX_WORDS} palabras")
        
#         return v

from pydantic import BaseModel, Field, field_validator
import re
from typing import Annotated

MAX_WORDS = 1000  # Aproximadamente 8000 tokens

from pydantic import BaseModel, Field, field_validator
import re
from typing import Annotated

MAX_WORDS = 1000  # Aproximadamente 8000 tokens

class ChatRequestSchema(BaseModel):
    session_id: str = Field(..., min_length=1, description="ID de sesión no puede estar vacío ni contener espacios")
    input: str = Field(..., min_length=1, description="Texto de entrada no puede estar vacío")

    @field_validator("session_id")
    @classmethod
    def validate_session_id(cls, v: str) -> str:
        """
        Valida que el session_id:
        1. No esté vacío
        2. No contenga espacios en blanco en ninguna posición
        3. No sea solo espacios en blanco
        """
        if not v:
            raise ValueError("El session_id no puede estar vacío")
            
        if v != v.strip():
            raise ValueError("El session_id no puede tener espacios al inicio o al final")
            
        if ' ' in v:
            raise ValueError("El session_id no puede contener espacios en medio")
            
        if re.search(r'\s', v):
            raise ValueError("El session_id no puede contener ningún tipo de espacio (tabs, newlines, etc.)")
            
        return v

    @field_validator("input")
    @classmethod
    def validate_input(cls, v: str) -> str:
        """Valida que el input no esté vacío y cumpla con el límite de palabras"""
        stripped = v.strip()
        
        if not stripped:
            raise ValueError("El input no puede estar vacío o contener solo espacios")
        
        words = stripped.split()
        if len(words) > MAX_WORDS:
            raise ValueError(f"El texto supera el límite de {MAX_WORDS} palabras")
        
        return v