import asyncio
from fastapi import FastAPI
from src.controllers.chat_controller import ChatController
from src.controllers.general_information_controller import GeneralInformationController
from src.controllers.thesis_import_controller import ThesisImportController
from src.controllers.thesis_vectorization_controller import ThesisVectorizationController
from src.database.chroma_database.thesis_collection import ThesisCollection
from src.database.postgres_database.chats.chats_repository import ChatWithPostgres, delete_old_messages
from src.database.postgres_database.thesis.init_db import AsyncSessionLocal
from src.database.postgres_database.thesis.process_status_repository import ProcessStatusRepository
from src.database.postgres_database.thesis.thesis_repository import ThesisRepository
from src.models.thesis_model import ProcessStatus
from src.security.auth import validate_api_key
from src.services.chat_service import ChatService
from src.agent.agent import AgentChatBot
from src.services.dspace_service import DSpaceService
from src.services.general_information_service import GeneralInformationService
# from src.services.thesis_data_importer_service import ThesisDataImporterService
from src.services.thesis_data_importer_service_copy import ThesisDataImporterService
from src.services.thesis_vectorization_service import ThesisVectorizationService
from src.services.thesis_vectorization_service_copy import ThesisVectorizationService
from src.services.book_metadata_service import BookMetadataService
from src.controllers.book_metadata_controller import BookMetadataController
from src.database.postgres_database.thesis.init_db import create_tables_async
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os
from dotenv import load_dotenv



class StartServer():

    def __init__(self):
        pass

    async def init_thesis_tables(self):
        await create_tables_async()

    async def change_running_processes_to_failed(self):
        async with AsyncSessionLocal() as session:
            repo = ProcessStatusRepository()
            running_processes = await repo.get_all_running_processes(session)
            print(f"🔎 Se encontraron {len(running_processes)} procesos en estado RUNNING.")
            for proc in running_processes:
                print(f"⚠️ Marcando como FAILED el proceso: {proc.process_name.value}")
                await repo.set_status(
                    session,
                    proc.process_name,
                    ProcessStatus.FAILED,
                    error_messages=["Fallo por cierre inesperado del servidor"]
                )

    def init_endpoints(self, app: FastAPI):
        self.init_book_metadata(app)
        self.init_chat(app)
        self.init_general_information(app)
        self.init_thesis_import(app)
        self.init_thesis_vectorization(app)
        
    def init_book_metadata(self, app: FastAPI):
        book_service = BookMetadataService()
        book_controller = BookMetadataController(book_service)
        app.include_router(book_controller.router, prefix="/books", tags=["Book Metadata"])

    def init_chat(self, app: FastAPI):
        chat_with_postgres = ChatWithPostgres()
        agent = AgentChatBot()  
        chat_service = ChatService(chat_with_postgres, agent)  
        chat_controller = ChatController(chat_service)
        app.include_router(chat_controller.router, prefix="/chat", tags=["Chat"])

    def init_general_information(self, app: FastAPI):
        general_info_service = GeneralInformationService()
        general_info_controller = GeneralInformationController(general_info_service)
        app.include_router(general_info_controller.router, prefix="/general-info", tags=["General Information"])

    def init_thesis_import(self, app: FastAPI):
        base_url_dspace = "https://repositorio.cujae.edu.cu/server/api"
        dspace_service = DSpaceService(base_url_dspace)
        thesis_repository = ThesisRepository()
        process_status_repository = ProcessStatusRepository()
        thesis_import_service = ThesisDataImporterService(dspace_service, thesis_repository, process_status_repository)
        thesis_import_controller = ThesisImportController(thesis_import_service)
        app.include_router(thesis_import_controller.router, prefix="/thesis-import", tags=["Thesis Import"])

    def init_thesis_vectorization(self, app: FastAPI):
        thesis_collection = ThesisCollection()
        thesis_repository = ThesisRepository()
        process_status_repository = ProcessStatusRepository()
        # thesis_vectorization_service = ThesisVectorizationService(thesis_collection, thesis_repository, process_status_repository)
        thesis_vectorization_service = ThesisVectorizationService(thesis_repository, process_status_repository)
        thesis_vectorization_controller = ThesisVectorizationController(thesis_vectorization_service)
        app.include_router(thesis_vectorization_controller.router, prefix="/thesis-vectorization", tags=["Thesis Vectorization"])


    #Esta función permite que de ser ENABLE_SCHEDULER = true en el archivo .env, se inicie el scheduler
    #para eliminar mensajes antiguos de la base de datos.
    #El scheduler se ejecuta en el horario definido por las variables SCHEDULE_DAY, SCHEDULE_HOUR y SCHEDULE_MINUTE
    #del archivo .env. Si no están definidas, se usan los valores por defecto: 1, 10 y 0 respectivamente.
    #El scheduler se ejecuta una vez al día, a la hora y minuto especificados
    #en el archivo .env.
    #El scheduler utiliza la función delete_old_messages para eliminar mensajes antiguos de la base de datos
    #de chats, que se define en ChatWithPostgres.
    def start_scheduler(self):
        # Carga variables del archivo .env al entorno
        load_dotenv()
        # Verificar si se debe habilitar el scheduler
        enable_scheduler = os.getenv("ENABLE_SCHEDULER", "false").lower() == "true"
        if not enable_scheduler:
            print(" Scheduler desactivado por configuración.")
            return

        # Leer variables y convertirlas a enteros
        day = int(os.getenv("SCHEDULE_DAY", 1))       # valor por defecto 1 si no está definido
        hour = int(os.getenv("SCHEDULE_HOUR", 10))     # valor por defecto 0
        minute = int(os.getenv("SCHEDULE_MINUTE", 0)) # valor por defecto 0

        scheduler = AsyncIOScheduler()
        scheduler.add_job(
            delete_old_messages,  # directamente la función async
            trigger='cron',
            day=day,
            hour=hour,
            minute=minute
        )
        scheduler.start()