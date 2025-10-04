from datetime import datetime
from typing import Optional

import sqlalchemy as sa
from pydantic import Json
from sqlalchemy.dialects.postgresql import JSON
from sqlmodel import SQLModel, Field


class LoggingEventBase(SQLModel):
    id: int = Field(primary_key=True, index=True, default=None)
    tan_code: str = Field(foreign_key="tan.code")
    timestamp: datetime = Field(sa_column=sa.Column(sa.DateTime(timezone=True), nullable=True))
    source: Optional[str] = Field(nullable=True, default=None)
    type: Optional[str] = Field(nullable=True, default=None)
    payload: Json = Field(sa_column=sa.Column(JSON))


class LoggingEvent(LoggingEventBase, table=True):
    __tablename__ = "logging_events"
