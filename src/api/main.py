from fastapi import FastAPI
from api.controllers import documents_controller
from database.vector_store import collection__of__books
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