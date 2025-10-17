import logging
from contextlib import asynccontextmanager

import aio_pika
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.config as conf
from app.api.v1 import health, logging_event, tan, exercise, grading_job
from app.db.database import create_tables


@asynccontextmanager
async def lifespan(_app: FastAPI):
    if conf.DEBUG:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    logging.info("create tables [start]")
    await create_tables()
    logging.info("create tables [done]")

    logging.info("setup message queue exchange [start]")

    mq_connection_str = f"amqp://{conf.MQ_USER}:{conf.MQ_PWD}@{conf.MQ_URL}:{conf.MQ_PORT}"
    connection = await aio_pika.connect_robust(mq_connection_str)

    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange(conf.MQ_EXCHANGE_NAME, 'topic', durable=True)
        queue = await channel.declare_queue(conf.GRADING_JOB_QUEUE, durable=True)

        await queue.bind(exchange, routing_key=conf.GRADING_JOB_ROUTING_KEY)
        await channel.close()

    logging.info("setup message queue exchange [done]")

    yield

    logging.info("shutting down...")


if conf.DEBUG:
    app = FastAPI(root_path=conf.BASE_URL, lifespan=lifespan)
else:
    app = FastAPI(root_path=conf.BASE_URL, docs_url=None, redoc_url=None, openapi_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=conf.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tan.router)
app.include_router(health.router)
app.include_router(logging_event.router)
app.include_router(exercise.router)
app.include_router(grading_job.router)
