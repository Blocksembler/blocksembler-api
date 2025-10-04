from datetime import datetime

import sqlalchemy as sa
from sqlmodel import SQLModel, Field, Column


class TAN(SQLModel, table=True):
    __tablename__ = "tan"

    code: str = Field(sa_column=Column(sa.String(), primary_key=True, nullable=False))
    valid_from: datetime | None = Field(sa_column=Column(sa.DateTime(timezone=True), nullable=True))
    valid_to: datetime | None = Field(sa_column=Column(sa.DateTime(timezone=True), nullable=True))
