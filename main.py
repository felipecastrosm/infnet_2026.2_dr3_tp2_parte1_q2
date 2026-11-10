from contextlib import asynccontextmanager

from fastapi import FastAPI

from routes import router
from services import get_translator


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_translator()
    yield


app = FastAPI(title="English to French Translation API", version="1.0.0", lifespan=lifespan)

app.include_router(router)
