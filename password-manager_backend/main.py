# main.py
from fastapi import FastAPI, Response, Request

from config import Container
from Presentation.Controllers.V1.LocalUserController import routerV1 as local_user_router_V1
from Presentation.Controllers.V1.SubAccountController import routerV1 as subaccount_router_V1
from Infrastructure.Repositories.Database import SessionLocal

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

@app.middleware("http")
async def DbSessionMiddleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    request.state.db = SessionLocal()
    try:
        response = await call_next(request)
        if request.method != "GET":
            request.state.db.commit()
    except Exception as e:
        request.state.db.rollback()
        raise e
    finally:
        request.state.db.close()
    return response

@app.middleware("http")
async def LogExceptionsMiddleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise e