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

KEYCLOAK_HOST = os.getenv("KEYCLOAK_HOST")
KEYCLOAK_PORT = os.getenv("KEYCLOAK_PORT")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
KEYCLOAK_AUDIENCE = os.getenv("KEYCLOAK_AUDIENCE")
KEYCLOAK_SECRET = os.getenv("KEYCLOAK_SECRET")

KEYCLOAK_URL = f"http://{KEYCLOAK_HOST}:{KEYCLOAK_PORT}/realms/{KEYCLOAK_REALM}"

# ------------------------------
# 🔑 Keycloak Config
# ------------------------------

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def VerifyToken(token: str = Depends(oauth2_scheme)):
    try:
        # Scarico chiavi pubbliche Keycloak
        jwks_url = f"{KEYCLOAK_URL}/protocol/openid-connect/certs"
        jwks = requests.get(jwks_url).json()

        # Estraggo header per kid
        header = jwt.get_unverified_header(token)
        key = next(k for k in jwks["keys"] if k["kid"] == header["kid"])

        # Decodifico token
        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=KEYCLOAK_AUDIENCE,
            issuer=f"{KEYCLOAK_URL}"
        )
        return payload
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token non valido o scaduto",
            headers={"WWW-Authenticate": "Bearer"},
        )

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

# 🔒 Router protetti con Keycloak
app.include_router(
    local_user_router_V1,
    prefix="/api/V1/localuser",
    tags=["LocalUser"],
    dependencies=[Depends(VerifyToken)]
)

app.include_router(
    subaccount_router_V1,
    prefix="/api/V1/subaccount",
    tags=["SubAccount"],
    dependencies=[Depends(VerifyToken)]
)

app.include_router(
    local_user_router_V2,
    prefix="/api/V2/localuser",
    tags=["LocalUser"],
    dependencies=[Depends(VerifyToken)]
)

app.include_router(
    subaccount_router_V2,
    prefix="/api/V2/subaccount",
    tags=["SubAccount"],
    dependencies=[Depends(VerifyToken)]
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

@app.middleware("http")
async def AuthMiddleware(request: Request, call_next):
    if request.url.path in ["/docs", "/openapi.json", "/redoc"]:
        return await call_next(request)

    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return Response("Token mancante", status_code=401)

    try:
        payload = VerifyToken(token.split(" ")[1])
        request.state.user = payload
    except HTTPException:
        return Response("Token non valido", status_code=401)

    return await call_next(request)
