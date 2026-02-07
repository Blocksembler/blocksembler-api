from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ExerciseCreate(BaseModel):
    title: str
    markdown: str
    skip_delay: int
    next_exercise_id: Optional[int]


class ExerciseRead(ExerciseCreate):
    id: int


class ExerciseWithUnlockTimestamps(ExerciseRead):
    skip_unlock_time: datetime
    next_grading_allowed_at: datetime


class SystemState(BaseModel):
    registers: dict[str, int]
    memory: dict[int, int]


class TestCaseCreate(BaseModel):
    title: str
    precondition: SystemState
    postcondition: SystemState
    user_input: list[str]
    expected_output: list[str]
    expected_instructions: list[str]
    step_limit: Optional[int] = None


class TestCaseRead(TestCaseCreate):
    id: int
