from datetime import datetime

from fastapi import HTTPException, APIRouter, status

from app.database import get_db
from app.schemas.logging import LoggingEvent
from app.schemas.tan import TanCode

router = APIRouter(
    prefix="/logging",
    tags=["logging"],
)


@router.get("/{tan_code}",
            response_model=list[LoggingEvent],
            status_code=status.HTTP_200_OK)
async def get_logging_events(tan_code: str) -> list[LoggingEvent]:
    db = await get_db()
    tan_result = await db.tans.find_one({'code': tan_code})

    if not tan_result:
        raise HTTPException(status_code=404, detail="TAN code not found")

    query = {
        'tan_code': tan_code,
    }

    events = await db.logging_events.find(query).sort('ts', -1).to_list()

    return [LoggingEvent(**event) for event in events]


@router.get("/{tan_code}/latest",
            response_model=LoggingEvent,
            status_code=status.HTTP_200_OK)
async def get_latest_logging_event(tan_code: str) -> LoggingEvent:
    # Verify that the TAN code exists
    db = await get_db()
    tan_result = await db.tans.find_one({'code': tan_code})

    if not tan_result:
        raise HTTPException(status_code=404, detail="TAN code not found")

    # Query for the latest event
    latest_event = await db.logging_events.find_one(
        {'tan_code': tan_code},
        sort=[('ts', -1)]  # Sort by timestamp descending
    )

    if not latest_event:
        raise HTTPException(status_code=404, detail="No logging events found for this TAN code")

    return LoggingEvent(**latest_event)


@router.post("/{tan_code}",
             response_model=int,
             status_code=status.HTTP_201_CREATED)
async def post_logging_events(tan_code: str, events: list[LoggingEvent]) -> int:
    db = await get_db()
    tan_result = await db.tans.find_one({'code': tan_code})

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
        result = await db.logging_events.insert_many(events_to_insert)
        return len(result.inserted_ids)
    return 0
