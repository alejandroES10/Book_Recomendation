from fastapi import FastAPI, Depends
from src.api.controllers import book_metadata_controller, chat_controller, general_information_controller
from fastapi.middleware.cors import CORSMiddleware
from src.api.security.auth import validate_api_key
from src.api.services.general_information_service import GeneralInformationService



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


app.include_router(book_metadata_controller.router, prefix="/materials")

app.include_router(chat_controller.router, prefix="/chat")
app.include_router(general_information_controller.router, prefix="/general_information",dependencies=[Depends(validate_api_key)])

# from fastapi import FastAPI


# app = FastAPI()
# book_controller = book_metadata_controller.BookController()
# app.include_router(book_controller.router, prefix="/books", tags=["Books"])

# general_information_controller = general_information_controller.GeneralInformationController()


# app.include_router(general_information_controller.router, prefix="/general-info")