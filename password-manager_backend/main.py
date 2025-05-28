from fastapi import FastAPI
from config import Container
from Presentation.Controllers.UserController import router

container = Container()
container.wire(modules=["Presentation.Controllers.UserController"])

app = FastAPI()

app.container = container

app.include_router(
    router,          
    prefix="/user",  
    tags=["user"]  
)