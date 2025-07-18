

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

# class BookMetadataSchema(BaseModel):
#     id: str = Field(
#         ...,
#         min_length=1,
#         pattern=r'^\S+$',
#         description="ID no puede tener espacios y debe tener al menos 1 carácter"
#     )
#     metadata: Dict[str, Union[str, int, float, bool]] = Field(
#         ...,
#         min_length=1,
#         description="Metadatos con claves válidas y valores permitidos (str, int, float, bool)"
#     )

#     @field_validator('metadata')
#     @classmethod
#     def validate_metadata(cls, value: Dict[str, Union[str, int, float, bool,list]]) -> Dict[str, Union[str, int, float, bool]]:
#         """Valida el diccionario de metadata incluyendo booleanos"""
#         if not value:
#             raise ValueError("El diccionario de metadata no puede estar vacío")
        
#         # Validación de claves
#         for key in value.keys():
#             if not key.strip():
#                 raise ValueError("Las claves no pueden ser cadenas vacías")
#             # if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', key):
#             #     raise ValueError(f"Clave '{key}' no válida. Solo letras, números y _")
#             if key.lower() in ['null', 'none']:
#                 raise ValueError(f"Clave '{key}' es una palabra reservada")
        
#         # Validación de valores
#         for key, val in value.items():
#             if val is None:
#                 raise ValueError(f"El valor para '{key}' no puede ser nulo")
#             if isinstance(val, str) and not val.strip():
#                 raise ValueError(f"Valor string vacío para '{key}'")
        
#         return value

from pydantic import BaseModel, field_validator
from typing import Dict, Any

class MetadataBaseSchema(BaseModel):
    
    metadata: Dict[str, Any]  # Accepts any value type except None/empty

    @field_validator('metadata')
    @classmethod
    def validate_metadata(cls, v):
        if not v:  # Check if metadata dict is empty
            raise ValueError("Metadata cannot be empty")
        
        for key, value in v.items():
            if not key or not key.strip():
                raise ValueError("Metadata keys cannot be empty")
            
            if value is None:
                raise ValueError(f"Metadata value for '{key}' cannot be None")
            
            if isinstance(value, (str, list, dict)) and not value:
                # Rejects empty strings/lists/dicts
                raise ValueError(f"Metadata value for '{key}' cannot be empty")
        
        return v
    

class BookCreateSchema(MetadataBaseSchema):
    id: str

    @field_validator('id')
    @classmethod
    def validate_id(cls, v):
        if not v:
            raise ValueError("ID cannot be empty")
            
        # Validación estricta sin espacios en ningún lugar
        if re.search(r'\s', v):
            raise ValueError("ID cannot contain any whitespace characters (spaces, tabs, etc.)")
            
        stripped = v.strip()
        if len(stripped) != len(v):
            raise ValueError("ID cannot have leading or trailing whitespace")
            
        return stripped
    
class BookUpdateSchema(MetadataBaseSchema):
    pass