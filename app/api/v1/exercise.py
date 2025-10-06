from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.models.exercise import ExerciseBase, Exercise

router = APIRouter(
    prefix="/exercise",
    tags=["exercise"],
)


@router.get("/{exercise_id}",
            response_model=ExerciseBase,
            status_code=status.HTTP_200_OK)
async def get_exercise(exercise_id: int, session: AsyncSession = Depends(get_session)) -> ExerciseBase:
    statement = select(Exercise).where(Exercise.id == exercise_id)
    result = await session.execute(statement)
    exercise = result.scalars().first()

    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    return exercise


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ExerciseBase)
async def create_exercise(exercise: ExerciseBase, session: AsyncSession = Depends(get_session)):
    db_exercise = Exercise(**exercise.model_dump())
    db_exercise.id = None

    session.add(db_exercise)
    await session.commit()

    return db_exercise
