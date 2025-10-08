import logging
from contextlib import asynccontextmanager

import amqp
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import health, logging_event, tan, exercise, grading
from app.config import BASE_URL, DEBUG, ORIGINS, MESSAGE_QUEUE_URL, MESSAGE_QUEUE_USER, MESSAGE_QUEUE_PASSWORD
from app.db.database import create_tables


@asynccontextmanager
async def lifespan(_app: FastAPI):
    if DEBUG:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    logging.info("create tables [start]")
    await create_tables()
    logging.info("create tables [done]")

    logging.info("setup message queue exchange [start]")
    with amqp.Connection(MESSAGE_QUEUE_URL, userid=MESSAGE_QUEUE_USER, password=MESSAGE_QUEUE_PASSWORD) as c:
        ch = c.channel()
        ch.exchange_declare('blocksembler-grading-exchange', 'topic', durable=True)
        ch.close()
    logging.info("setup message queue exchange [done]")

    yield

    logging.info("shutting down...")


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
app.include_router(logging_event.router)
app.include_router(exercise.router)
app.include_router(grading.router)
