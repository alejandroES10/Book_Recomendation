from contextlib import asynccontextmanager
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from src.start_server.start_server import StartServer


# import logging

# logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🌱 Lifespan startup comenzando...")

    start_server = StartServer()
    start_server.init_endpoints(app)
    await start_server.init_thesis_tables()
    await start_server.change_running_processes_to_failed()
    start_server.start_scheduler()

    print("✅ Lifespan startup completado.")
    yield

app = FastAPI(lifespan=lifespan)

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


