from amqp import Connection

from app.config import MESSAGE_QUEUE_URL, MESSAGE_QUEUE_USER, MESSAGE_QUEUE_PASSWORD


async def get_mq_connection() -> Connection:
    with Connection(MESSAGE_QUEUE_URL, userid=MESSAGE_QUEUE_USER, password=MESSAGE_QUEUE_PASSWORD) as c:
        yield c  # noqa
