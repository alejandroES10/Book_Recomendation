from fastapi import FastAPI
from api.controllers import search_controller

app = FastAPI()

@app.get("/")
async def read_root():
    return "Book Recomendation API"

app.include_router(search_controller.router, prefix="/search")