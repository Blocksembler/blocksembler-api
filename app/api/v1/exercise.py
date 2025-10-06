from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schema.exercise import ExerciseRead, ExerciseCreate
from app.db.database import get_session
from app.db.model.exercise import Exercise

router = APIRouter(
    prefix="/exercise",
    tags=["exercise"],
)


@router.get("/{exercise_id}",
            response_model=ExerciseRead,
            status_code=status.HTTP_200_OK)
async def get_exercise(exercise_id: int, session: AsyncSession = Depends(get_session)) -> ExerciseRead:
    statement = select(Exercise).where(Exercise.id == exercise_id)
    result = await session.execute(statement)
    exercise = result.scalars().first()

    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    return ExerciseRead(**exercise.to_dict())


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ExerciseRead)
async def create_exercise(new_exercise: ExerciseCreate, session: AsyncSession = Depends(get_session)) -> ExerciseRead:
    exercise = Exercise(**new_exercise.model_dump())
    exercise.id = None

    session.add(exercise)
    await session.commit()

    return ExerciseRead(**exercise.to_dict())
