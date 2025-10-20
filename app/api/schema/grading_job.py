from datetime import datetime

from pydantic import BaseModel


class ExerciseSubmission(BaseModel):
    tan_code: str
    exercise_id: int
    solution_code: str


class GradingJobRead(BaseModel):
    id: str
    tan_code: str
    exercise_id: int
    status: str
    started: datetime
    terminated: datetime | None
    passed: bool | None
    feedback: list[str] | None
