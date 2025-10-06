from pydantic import BaseModel


class ExerciseCreate(BaseModel):
    title: str
    markdown: str
    coding_mode: str


class ExerciseRead(ExerciseCreate):
    id: int
