from fastapi import FastAPI, Depends
from src.api.controllers import chat_controller, general_information_controller, material_controller
from fastapi.middleware.cors import CORSMiddleware
from src.api.security.auth import validate_api_key



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,  
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.get("/")
async def read_root():
    return "Tesis de Alejandro Estrada Suárez"


app.include_router(material_controller.router, prefix="/materials",dependencies=[Depends(validate_api_key)])

app.include_router(chat_controller.router, prefix="/chat",dependencies=[Depends(validate_api_key)])
app.include_router(general_information_controller.router, prefix="/general_information",dependencies=[Depends(validate_api_key)])