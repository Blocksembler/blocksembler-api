from datetime import datetime

from pydantic import BaseModel, Field


class TanCreationRequest(BaseModel):
    count: int = Field(description="The number of tan codes that should be created", lt=100)
    valid_from: datetime = Field(description="The date and time from which the generated TAN codes become valid.")
    valid_to: datetime | None = Field(description="The date and time until the generated TAN codes remain valid.", default=None)


class TanCode(BaseModel):
    code: str = Field(description="Alphanumeric tan code")
    valid_from: datetime = Field(description="The date and time from which the TAN code becomes valid.",
                                 default_factory=datetime.now)
    valid_to: datetime | None = Field(description="The date and time until the TAN code remains valid.")


class LoggingEvent(BaseModel):
    ts: datetime = Field(description="The date and time of the log", default_factory=datetime.now)
    type: str = Field(description="Logging type")
    source: str = Field(description="Source of the log")
    payload: dict = Field(description="Logging payload", default_factory=dict)
