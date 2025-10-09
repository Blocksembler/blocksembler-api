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


class SystemState(BaseModel):
    registers: dict[str, int]
    memory: dict[int, int]


class TestCaseCreate(BaseModel):
    title: str
    precondition: SystemState
    postcondition: SystemState
    user_input: list[str]
    expected_output: list[str]


class TestCaseRead(TestCaseCreate):
    id: int
