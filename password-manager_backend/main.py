from fastapi import FastAPI
from config import Container
from Presentation.Controllers.LocalUserController import router as local_user_router

container = Container()
container.wire(modules=["Presentation.Controllers.LocalUserController"])

app = FastAPI()

app.container = container

app.include_router(
    local_user_router,          
    prefix="/user",  
    tags=["user"]  
)