from fastapi import FastAPI, Depends
from src.controllers import book_metadata_controller, chat_controller, general_information_controller
from fastapi.middleware.cors import CORSMiddleware
from src.database.postgres.chats.chats_repository import ChatWithPostgres
from src.security.auth import validate_api_key
from src.services.chat_service import ChatService
from src.chatbot.agent import AgentChatBot




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


from src.services.book_metadata_service import BookMetadataService
from src.controllers.book_metadata_controller import BookMetadataController

app = FastAPI()

service = BookMetadataService()
book_controller = BookMetadataController(service)


chat_with_postgres = ChatWithPostgres()
agent = AgentChatBot()  # Asegúrate de que tienes una instancia de tu agente
chat_service = ChatService(chat_with_postgres,agent)  # instancia concreta que implementa IChatService
chat_controller = chat_controller.ChatController(chat_service)

app.include_router(book_controller.router, prefix="/books", tags=["Book Metadata"])
app.include_router(chat_controller.router, prefix="/chat", tags=["Chat"])


# app.include_router(book_metadata_controller.router, prefix="/materials")

# app.include_router(chat_controller.router, prefix="/chat")
# app.include_router(general_information_controller.router, prefix="/general-information",dependencies=[Depends(validate_api_key)])

# from fastapi import FastAPI


# app = FastAPI()
# book_controller = book_metadata_controller.BookController()
# app.include_router(book_controller.router, prefix="/books", tags=["Books"])

# general_information_controller = general_information_controller.GeneralInformationController()


# app.include_router(general_information_controller.router, prefix="/general-info")