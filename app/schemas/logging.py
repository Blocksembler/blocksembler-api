from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field, Json


class LoggingEvent(BaseModel):
    tan_code: Optional[str] = Field(description="The tan code of the TAN code", default=None)
    timestamp: datetime = Field(description="The date and time of the log", default_factory=datetime.now)
    source: str = Field(description="Source of the log")
    type: str = Field(description="Logging type")
    payload: Json[Any] = Field(description="Logging payload", default_factory=dict)
