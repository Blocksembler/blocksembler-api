from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import health, logging, tan, exercise
from app.config import BASE_URL, DEBUG, ORIGINS
from app.database import create_tables


@asynccontextmanager
async def lifespan(_app: FastAPI):
    print("create tables ...")
    await create_tables()
    print("create tables [done]")
    yield


if DEBUG:
    app = FastAPI(root_path=BASE_URL, lifespan=lifespan)
else:
    app = FastAPI(root_path=BASE_URL, docs_url=None, redoc_url=None, openapi_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tan.router)
app.include_router(health.router)
app.include_router(logging.router)
app.include_router(exercise.router)
