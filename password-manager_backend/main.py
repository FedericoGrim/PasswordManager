# main.py
from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from config import Container
from Presentation.Controllers.LocalUserController import router as local_user_router
from Presentation.Controllers.SubAccountController import router as subaccount_router
from Infrastructure.Databases.SQL.Database import SessionLocal
from Infrastructure.Databases.NoSQL.Models import UserEvent

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
container.wire(modules=["Presentation.Controllers.LocalUserController", "Presentation.Controllers.SubAccountController"])

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inizializza Motor client e registra nel container DI
client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
container.NoSQL.events().mongo_client.override(client)
app.container = container

app.include_router(
    local_user_router,
    prefix="/api/localuser",
    tags=["LocalUser"],
)

app.include_router(
    subaccount_router,
    prefix="/api/subaccount",
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

@app.on_event("startup")
async def startup_event():
    try:
        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri:
            print("⚠️  MONGO_URI not set in .env")
            return
        
        print(f"🔌 Connecting to MongoDB at {mongo_uri}...")
        client = AsyncIOMotorClient(mongo_uri, serverSelectionTimeoutMS=5000)
        db = client.get_database(os.getenv("MONGO_DB_NAME"))
        
        # Test connection
        await db.command("ping")
        print("✅ MongoDB connected successfully")
        
        await init_beanie(database=db, document_models=[UserEvent])
        print("✅ Beanie initialized successfully")
    except Exception as e:
        print(f"❌ MongoDB initialization failed: {str(e)}")
        print("⚠️  Events will not be saved. Check your MONGO_URI in .env")
        # Non solleva eccezione per permettere all'app di partire anche senza MongoDB
        # Commenta il return qui sotto se vuoi che l'app fallisca senza MongoDB
        # raise e
