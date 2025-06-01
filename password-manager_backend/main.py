# main.py
from fastapi import FastAPI
from config import Container
from Presentation.Controllers.LocalUserController import router as local_user_router
from Presentation.Controllers.SubaccountController import router as subaccount_router

container = Container()
container.wire(modules=["Presentation.Controllers.LocalUserController", "Presentation.Controllers.SubaccountController"])

app = FastAPI()

# Assegno i container al FastAPI app per accedervi dal controller
app.container = container

app.include_router(
    local_user_router,
    prefix="/user",
    tags=["user"]
)

app.include_router(
    subaccount_router,
    prefix="/subaccounts",
    tags=["subaccounts"]
)
