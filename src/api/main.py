from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
# from src.controllers import book_metadata_controller, chat_controller, general_information_controller
from fastapi.middleware.cors import CORSMiddleware
from src.controllers.chat_controller import ChatController
from src.controllers.general_information_controller import GeneralInformationController
from src.controllers.thesis_import_controller import ThesisImportController
from src.controllers.thesis_vectorization_controller import ThesisVectorizationController
from src.database.chromadb.thesis_collection import ThesisCollection
from src.database.postgres.chats.chats_repository import ChatWithPostgres
from src.database.postgres.thesis.init_db import AsyncSessionLocal
from src.database.postgres.thesis.process_status_repository import ProcessStatusRepository
from src.database.postgres.thesis.thesis_repository import ThesisRepository
from src.models.thesis_model import ProcessStatus
from src.security.auth import validate_api_key
from src.services.chat_service import ChatService
from src.chatbot.agent import AgentChatBot
from src.services.dspace_service import DSpaceService
from src.services.general_information_service import GeneralInformationService
from src.services.thesis_data_importer_service import ThesisDataImporterService
from src.services.thesis_vectorization_service import ThesisVectorizationService

import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🌱 Lifespan startup comenzando...")

    async with AsyncSessionLocal() as session:
        repo = ProcessStatusRepository()
        running_processes = await repo.get_all_running_processes(session)
        logger.info(f"🔎 Se encontraron {len(running_processes)} procesos en estado RUNNING.")
        for proc in running_processes:
            logger.info(f"⚠️ Marcando como FAILED el proceso: {proc.process_name.value}")
            await repo.set_status(
                session,
                proc.process_name,
                ProcessStatus.FAILED,
                error_messages=["Fallo por cierre inesperado del servidor"]
            )

    logger.info("✅ Lifespan startup completado.")
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


from src.services.book_metadata_service import BookMetadataService
from src.controllers.book_metadata_controller import BookMetadataController

# app = FastAPI()

service = BookMetadataService()
book_controller = BookMetadataController(service)


chat_with_postgres = ChatWithPostgres()
agent = AgentChatBot()  
chat_service = ChatService(chat_with_postgres,agent)  
chat_controller = ChatController(chat_service)

general_info_service = GeneralInformationService()
general_info_controller = GeneralInformationController(general_info_service)

base_url_dspace="https://repositorio.cujae.edu.cu/server/api"
dspace_service = DSpaceService(base_url_dspace)
thesis_repository = ThesisRepository()
process_status_repository = ProcessStatusRepository()
thesis_import_service = ThesisDataImporterService(dspace_service, thesis_repository,process_status_repository)
thesis_import_controller = ThesisImportController(thesis_import_service)

thesis_collection = ThesisCollection()
thesis_vectorization_service = ThesisVectorizationService(thesis_collection, thesis_repository, process_status_repository)
thesis_vectorization_controller = ThesisVectorizationController(thesis_vectorization_service)

app.include_router(book_controller.router, prefix="/books", tags=["Book Metadata"])
app.include_router(chat_controller.router, prefix="/chat", tags=["Chat"])
app.include_router(general_info_controller.router, prefix="/general-info", tags=["General Information"])
app.include_router(thesis_import_controller.router, prefix="/thesis-import", tags=["Thesis Import"])
app.include_router(thesis_vectorization_controller.router, prefix="/thesis-vectorization", tags=["Thesis Vectorization"])

# app.include_router(book_metadata_controller.router, prefix="/materials")

# app.include_router(chat_controller.router, prefix="/chat")
# app.include_router(general_information_controller.router, prefix="/general-information",dependencies=[Depends(validate_api_key)])

# from fastapi import FastAPI


# app = FastAPI()
# book_controller = book_metadata_controller.BookController()
# app.include_router(book_controller.router, prefix="/books", tags=["Books"])

# general_information_controller = general_information_controller.GeneralInformationController()


# app.include_router(general_information_controller.router, prefix="/general-info")