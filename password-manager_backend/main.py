# main.py
from fastapi import FastAPI, Response, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
import requests

from config import Container
from Presentation.Controllers.V1.LocalUserController import routerV1 as local_user_router_V1
from Presentation.Controllers.V1.SubAccountController import routerV1 as subaccount_router_V1
from Presentation.Controllers.V2.LocalUserController import routerV2 as local_user_router_V2
from Presentation.Controllers.V2.SubAccountController import routerV2 as subaccount_router_V2
from Infrastructure.Repositories.Database import SessionLocal

from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# ------------------------------
# FastAPI App
# ------------------------------
container = Container()
container.wire(modules=["Presentation.Controllers.V1.LocalUserController", "Presentation.Controllers.V1.SubAccountController"])

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.container = container

app.include_router(
    local_user_router_V1,
    prefix="/api/V1/localuser",
    tags=["LocalUser"],
)

app.include_router(
    subaccount_router_V1,
    prefix="/api/V1/subaccount",
    tags=["SubAccount"],
)

app.include_router(
    local_user_router_V2,
    prefix="/api/V2/localuser",
    tags=["LocalUser"],
)

app.include_router(
    subaccount_router_V2,
    prefix="/api/V2/subaccount",
    tags=["SubAccount"],
)

# ------------------------------
# Middlewares DB + Log
# ------------------------------
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
