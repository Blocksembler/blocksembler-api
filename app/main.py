import os
import random
import string
from datetime import datetime
from typing import Any

from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from starlette import status

from app.schemas import TanCode, LoggingEvent, TanCreationRequest

DB_URL = os.environ.get('BLOCKSEMBLER_API_DB_URL', 'localhost')
DB_PORT = int(os.environ.get('BLOCKSEMBLER_API_DB_PORT', 27017))

if os.environ.get('DEBUG', True):
    print(f"Using database at {DB_URL}:{DB_PORT}")

BASE_URL = os.environ.get('BLOCKSEMBLER_API_BASE_URL', '')

client = MongoClient(DB_URL, DB_PORT)

if os.environ.get('DEBUG', True):
    app = FastAPI(root_path=BASE_URL)
else:
    app = FastAPI(root_path=BASE_URL, docs_url=None, redoc_url=None, openapi_url=None)


def generate_tan(length=6):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))


@app.get("/health")
async def health_check() -> dict:
    try:
        client.admin.command('ping')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Can't connect to database")
    return {"status": "ok"}


@app.get("/tan/{code}",
         response_model=TanCode,
         status_code=status.HTTP_200_OK)
async def get_tan_code(code: str) -> Any:
    db = client.blocksembler
    result = db.tans.find_one({'code': code})

    if not result:
        raise HTTPException(status_code=404, detail="Item not found")

    return TanCode(**result)


@app.get("/logging/{tan_code}",
         response_model=list[LoggingEvent],
         status_code=status.HTTP_200_OK)
async def get_logging_events(tan_code: str, start: datetime, end: datetime | None = None) -> list[LoggingEvent]:
    db = client.blocksembler
    tan_result = db.tans.find_one({'code': tan_code})

    if not tan_result:
        raise HTTPException(status_code=404, detail="TAN code not found")

    query = {
        'tan_code': tan_code,
        'ts': {'$gte': start}
    }

    if end:
        query['ts']['$lte'] = end

    events = list(db.logging_events.find(query).sort('ts', -1))

    return [LoggingEvent(**event) for event in events]


@app.get("/logging/{tan_code}/latest",
         response_model=LoggingEvent,
         status_code=status.HTTP_200_OK)
async def get_latest_logging_event(tan_code: str) -> LoggingEvent:
    # Verify that the TAN code exists
    db = client.blocksembler
    tan_result = db.tans.find_one({'code': tan_code})

    if not tan_result:
        raise HTTPException(status_code=404, detail="TAN code not found")

    # Query for the latest event
    latest_event = db.logging_events.find_one(
        {'tan_code': tan_code},
        sort=[('ts', -1)]  # Sort by timestamp descending
    )

    if not latest_event:
        raise HTTPException(status_code=404, detail="No logging events found for this TAN code")

    return LoggingEvent(**latest_event)


@app.post("/logging/{tan_code}",
          response_model=int,
          status_code=status.HTTP_201_CREATED)
async def post_logging_events(tan_code: str, events: list[LoggingEvent]) -> int:
    db = client.blocksembler
    tan_result = db.tans.find_one({'code': tan_code})

    if not tan_result:
        raise HTTPException(status_code=404, detail="TAN code not found")

    tan = TanCode(**tan_result)
    now = datetime.now()

    if tan.valid_from > now:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid TAN code")

    if tan.valid_to and tan.valid_to < now:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"TAN code expired on {tan.valid_to}")

    events_to_insert = []
    for event in events:
        event_dict = event.model_dump()
        event_dict['tan_code'] = tan_code
        events_to_insert.append(event_dict)

    if events_to_insert:
        result = db.logging_events.insert_many(events_to_insert)
        return len(result.inserted_ids)
    return 0
