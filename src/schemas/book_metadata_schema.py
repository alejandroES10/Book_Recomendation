
from pydantic import BaseModel, Field, validator

# class BookMetadataSchema(BaseModel):
#     id: str 
#     # page_content: str
#     metadata: dict
  
from pydantic import BaseModel, Field, field_validator
from typing import Dict, Union
from fastapi import HTTPException

from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Dict, Union, Literal
import re

from pydantic import BaseModel, Field, field_validator
from typing import Dict, Union
import re

class BookMetadataSchema(BaseModel):
    id: str = Field(
        ...,
        min_length=1,
        pattern=r'^\S+$',
        description="ID no puede tener espacios y debe tener al menos 1 carácter"
    )
    metadata: Dict[str, Union[str, int, float, bool]] = Field(
        ...,
        min_length=1,
        description="Metadatos con claves válidas y valores permitidos (str, int, float, bool)"
    )

    @field_validator('metadata')
    @classmethod
    def validate_metadata(cls, value: Dict[str, Union[str, int, float, bool]]) -> Dict[str, Union[str, int, float, bool]]:
        """Valida el diccionario de metadata incluyendo booleanos"""
        if not value:
            raise ValueError("El diccionario de metadata no puede estar vacío")
        
        # Validación de claves
        for key in value.keys():
            if not key.strip():
                raise ValueError("Las claves no pueden ser cadenas vacías")
            if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', key):
                raise ValueError(f"Clave '{key}' no válida. Solo letras, números y _")
            if key.lower() in ['null', 'none']:
                raise ValueError(f"Clave '{key}' es una palabra reservada")
        
        # Validación de valores
        for key, val in value.items():
            if val is None:
                raise ValueError(f"El valor para '{key}' no puede ser nulo")
            if isinstance(val, str) and not val.strip():
                raise ValueError(f"Valor string vacío para '{key}'")
        
        return value