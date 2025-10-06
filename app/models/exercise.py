import sqlalchemy as sa
from sqlmodel import SQLModel, Field


class ExerciseBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    markdown: str = Field(sa_column=sa.Column(sa.TEXT, nullable=False))
    coding_mode: str


class Exercise(ExerciseBase, table=True):
    __tablename__ = 'exercise'
