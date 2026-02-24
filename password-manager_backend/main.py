# main.py
from fastapi import FastAPI, Response, Request
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie # type: ignore[misc]
from starlette.middleware.base import RequestResponseEndpoint

from config import Container
from Presentation.Controllers.UserController import router as user_router
from Presentation.Controllers.SubAccountController import router as subaccount_router
from Presentation.Controllers.TeamController import router as team_router
from Presentation.Controllers.TeamMembersController import router as team_members_router
from Presentation.Controllers.CategoriesController import router as categories_router
from Presentation.Controllers.SubAccountCategoriesController import router as subacc_categories_router

from Infrastructure.Databases.SQL.Database import SessionLocal
from Domain.EventsPayload.Models import UserEvent

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
container.wire(modules=["Presentation.Controllers.UserController", 
                        "Presentation.Controllers.SubAccountController", 
                        "Presentation.Controllers.TeamController",
                        "Presentation.Controllers.TeamMembersController",
                        "Presentation.Controllers.CategoriesController",
                        "Presentation.Controllers.SubAccountCategoriesController"
                        ])

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = AsyncIOMotorClient(os.getenv("MONGO_URI")) # type: ignore[misc]
container.NoSQL.events().mongo_client.override(client)  # type: ignore[misc]
app.state.container = container

app.include_router(
    user_router,
    prefix="/api/user",
    tags=["User"],
)

app.include_router(
    subaccount_router,
    prefix="/api/subaccount",
    tags=["SubAccount"],
)

app.include_router(
    team_router,
    prefix="/api/team",
    tags=["Team"],
)

app.include_router(
    team_members_router,
    prefix="/api/team-members",
    tags=["TeamMembers"],
)

app.include_router(
    categories_router,
    prefix="/api/categories",
    tags=["Categories"],
)

app.include_router(
    subacc_categories_router,
    prefix="/api/subaccount-categories",
    tags=["SubAccountCategories"],
)

# ------------------------------
# Middlewares DB + Log
# ------------------------------
@app.middleware("http")
async def DbSessionMiddleware(request: Request, call_next: RequestResponseEndpoint):
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
async def LogExceptionsMiddleware(request: Request, call_next: RequestResponseEndpoint):
    try:
        response = await call_next(request)
        return response
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise e

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --------- STARTUP ---------
    try:
        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri:
            print("⚠️  MONGO_URI not set in .env")
        else:
            print(f"🔌 Connecting to MongoDB at {mongo_uri}...")
            client = AsyncIOMotorClient(mongo_uri, serverSelectionTimeoutMS=5000)  # type: ignore[misc]
            db = client.get_database(os.getenv("MONGO_DB_NAME"))  # type: ignore[misc]
            
            await db.command("ping")
            print("✅ MongoDB connected successfully")
            
            await init_beanie(database=db, document_models=[UserEvent])  # type: ignore[misc]
            print("✅ Beanie initialized successfully")

    except Exception as e:
        print(f"❌ MongoDB initialization failed: {str(e)}")
        print("⚠️  Events will not be saved. Check your MONGO_URI in .env")

    yield  # l'app gira qui

    # --------- SHUTDOWN ---------
    print("🔌 Shutting down...")