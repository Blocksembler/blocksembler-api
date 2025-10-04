import datetime

from fastapi import HTTPException, APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.models.logging import LoggingEvent, LoggingEventBase
from app.models.tan import TAN

router = APIRouter(
    prefix="/logging",
    tags=["logging"],
)


@router.get("/{tan_code}",
            response_model=list[LoggingEventBase],
            status_code=status.HTTP_200_OK)
async def get_logging_events(tan_code: str, session: AsyncSession = Depends(get_session)) -> list[LoggingEvent]:
    statement = select(TAN).where(TAN.code == tan_code)
    result = await session.execute(statement)
    tan = result.scalars().first()

    if not tan:
        raise HTTPException(status_code=404, detail="TAN code not found")

    statement = select(LoggingEvent).where(LoggingEvent.tan_code == tan_code)
    result = await session.execute(statement)

    return [event for event in result.scalars().all()]


@router.post("/{tan_code}",
             response_model=int,
             status_code=status.HTTP_201_CREATED)
async def post_logging_events(tan_code: str, events: list[LoggingEventBase],
                              session: AsyncSession = Depends(get_session)) -> int:
    statement = select(TAN).where(TAN.code == tan_code)
    result = await session.execute(statement)
    tan = result.scalars().first()

    if not tan:
        raise HTTPException(status_code=404, detail="TAN code not found")

    now = datetime.datetime.now(datetime.UTC)

    if tan.valid_from and tan.valid_from > now:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid TAN code")

    if tan.valid_to and tan.valid_to < now:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"TAN code expired on {tan.valid_to}")

    for event in events:
        event.tan_code = tan_code

    if events:
        session.add_all([LoggingEvent(**event.model_dump()) for event in events])
        await session.commit()
        return len(events)
    return 0
