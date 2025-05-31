from fastapi import Security, HTTPException, status, Depends
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv
import os
import hmac

# Cargar variables de entorno
load_dotenv()
API_KEY_SECURE = os.getenv("API_KEY_SECURE")

# Validar que la API Key está configurada antes de iniciar el servidor
if not API_KEY_SECURE:
    raise ValueError("API_KEY no está configurada en las variables de entorno")

# Configurar encabezado de autenticación
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def validate_api_key(api_key: str = Security(api_key_header)) -> None:
    """
    Valida la API Key con una comparación segura.
    """
    if not api_key or not hmac.compare_digest(api_key, API_KEY_SECURE):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autorizado",
            headers={"WWW-Authenticate": "API-Key"},
        )
