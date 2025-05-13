from fastapi import FastAPI, Request
from Presentation.UserAPI import router as user_router
import time
import logging

app = FastAPI()

@app.middleware("http")
async def LogRequestMiddleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    logging.info(f"{request.method} {request.url.path} - {response.status_code} - {duration:.2f}s")
    return response

app.include_router(user_router, prefix="/users", tags=["user"])