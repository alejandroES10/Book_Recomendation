from fastapi import FastAPI
from src.api.controllers import chat_controller, general_information_controller, material_controller
from fastapi.middleware.cors import CORSMiddleware

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
    return "Book Recomendation"


app.include_router(material_controller.router, prefix="/materials")
app.include_router(chat_controller.router, prefix="/chat")
app.include_router(general_information_controller.router, prefix="/general_information")