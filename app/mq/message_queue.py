import aio_pika
from aio_pika.abc import AbstractRobustChannel


async def get_mq_channel() -> AbstractRobustChannel:
    connection = await aio_pika.connect_robust("amqp://blocksembler:blocksembler@localhost:5672")

    async with connection:
        channel = await connection.channel()
        yield channel
