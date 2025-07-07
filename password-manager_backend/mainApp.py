# main.py
from fastapi import FastAPI
from config import Container
from Presentation.Controllers.V1.LocalUserController import routerV1 as local_user_router_V1
from Presentation.Controllers.V1.SubAccountController import routerV1 as subaccount_router_V1

container = Container()
container.wire(modules=["Presentation.Controllers.V1.LocalUserController", "Presentation.Controllers.V1.SubAccountController"])

app = FastAPI()

# Assegno i container al FastAPI app per accedervi dal controller
app.container = container

app.include_router(
    local_user_router_V1,
    prefix="/api/V1/localuser",
    tags=["LocalUser"]
)

app.include_router(
    subaccount_router_V1,
    prefix="/api/V1/subaccount",
    tags=["SubAccount"]
)
