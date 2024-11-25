from fastapi import FastAPI
from src.api.controllers import documents_controller, chat_controller
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


app.include_router(documents_controller.router, prefix="/documents")
app.include_router(chat_controller.router, prefix="/chat")