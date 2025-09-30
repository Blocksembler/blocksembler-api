import os
from typing import Optional

from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

MONGO_URI = os.environ.get("BLOCKSEMBLER_API_DB_URL", "mongodb://localhost:27017")
MONGO_DB_NAME = os.environ.get("BLOCKSEMBLER_API_DB_NAME", "blocksembler")

_client: Optional[AsyncMongoClient] = None
_db: Optional[AsyncDatabase] = None


async def get_client():
    global _client

    if _client is None:
        _client = AsyncMongoClient(MONGO_URI)

    return _client


async def close_mongo_connection():
    global _client
    if _client is not None:
        await _client.close()


async def get_db() -> AsyncDatabase:
    global _db

    if _db is None:
        client = await get_client()
        _db = client[MONGO_DB_NAME]

    return _db
