from datetime import datetime
from typing import Optional

from pydantic import Json, BaseModel


class LoggingEventCreate(BaseModel):
    tan_code: str
    timestamp: datetime
    source: Optional[str]
    type: Optional[str]
    payload: Json


class LoggingEventRead(LoggingEventCreate):
    id: int
