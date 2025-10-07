from typing import Optional

from pydantic import BaseModel


class ExerciseCreate(BaseModel):
    title: str
    markdown: str
    coding_mode: str
    allow_skip_after: Optional[int]
    next_exercise_id: Optional[int]


class ExerciseRead(ExerciseCreate):
    id: int
