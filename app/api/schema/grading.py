from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ExerciseSubmission(BaseModel):
    tan_code: str
    exercise_id: int
    solution_code: str


class GradingResult(BaseModel):
    success: bool
    penalty: datetime
    feedback: str
    hint: Optional[str]


class GradingJobRead(BaseModel):
    id: str
    tan_code: str
    exercise_id: int
    status: str
    started: datetime
    terminated: datetime | None
    passed: bool | None
    feedback: GradingResult | None
