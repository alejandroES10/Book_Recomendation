from fastapi import FastAPI
from api.controllers import search_controller, documents_controller
from database.vector_store import collection__of__books

app = FastAPI()

@app.get("/")
async def read_root():
    return "Books Recomendation"


app.include_router(documents_controller.router, prefix="/documents")