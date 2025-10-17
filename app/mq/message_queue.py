import logging

import aio_pika
from aio_pika.abc import AbstractRobustChannel

from app.config import MQ_USER, MQ_PWD, MQ_PORT, MQ_URL


async def get_mq_channel() -> AbstractRobustChannel:
    uri = f"amqp://{MQ_USER}:{MQ_PWD}@{MQ_URL}:{MQ_PORT}"
    logging.debug('connect to: ', uri)
    connection = await aio_pika.connect_robust(uri)

    async with connection:
        channel = await connection.channel()
        yield channel
