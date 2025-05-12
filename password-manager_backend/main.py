from fastapi import FastAPI

from Presentation.UserAPI import router as user_router

App = FastAPI()

App.include_router(user_router, prefix="/users", tags=["user"])