import datetime

import sqlalchemy as sa
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schema.exercise import ExerciseRead, ExerciseCreate, TestCaseRead, TestCaseCreate
from app.db.database import get_session
from app.db.model import Tan
from app.db.model.exercise import Exercise, ExerciseProgress, Competition, TestCase

router = APIRouter(
    prefix="/exercise",
    tags=["exercise"],
)


@router.get("/current",
            response_model=ExerciseRead,
            status_code=status.HTTP_200_OK)
async def get_current_exercise(tan_code: str, session: AsyncSession = Depends(get_session)) -> ExerciseRead:
    statement = select(Tan).where(Tan.code == tan_code)
    result = await session.execute(statement)
    tan = result.scalars().first()

    if not tan:
        raise HTTPException(status_code=404, detail="TAN code not found")

    statement = (select(Exercise)
                 .where(Exercise.id == (select(ExerciseProgress.exercise_id)
                                        .where(sa.and_(ExerciseProgress.tan_code == tan_code,
                                                       ExerciseProgress.end_time.is_(None)))
                                        .scalar_subquery())))

    result = await session.execute(statement)
    exercise = result.scalars().first()

    if not exercise:
        subquery = (
            select(ExerciseProgress.exercise_id)
            .where(ExerciseProgress.tan_code.like(tan_code))
        )

        stmt = (
            select(Exercise)
            .join(ExerciseProgress, ExerciseProgress.exercise_id == Exercise.id)
            .where(sa.and_(
                ExerciseProgress.tan_code.like(tan_code)),
                ~Exercise.next_exercise_id.in_(subquery),
                Exercise.id.in_(subquery)
            )
        )

        result = await session.execute(stmt)
        last_exercise = result.scalars().first()

        if last_exercise:
            ep = ExerciseProgress(
                tan_code=tan_code,
                exercise_id=last_exercise.next_exercise_id,
                start_time=datetime.datetime.now(),
                skipped=False
            )
            session.add(ep)
            await session.commit()
            await session.refresh(last_exercise)

            stmt = select(Exercise).where(Exercise.id == last_exercise.next_exercise_id)
            result = await session.execute(stmt)
            exercise = result.scalars().first()
            return ExerciseRead(**exercise.to_dict())

        else:
            stmt = (select(Competition)
                    .join(Tan, Tan.competition_id == Competition.id)
                    .where(Tan.code == tan_code))
            result = await session.execute(stmt)
            first_exercise_id = result.scalars().first().first_exercise_id

            ep = ExerciseProgress(
                tan_code=tan_code,
                exercise_id=first_exercise_id,
                start_time=datetime.datetime.now(),
                skipped=False
            )

            session.add(ep)
            await session.commit()

            stmt = select(Exercise).where(Exercise.id == first_exercise_id)
            result = await session.execute(stmt)
            exercise = result.scalars().first()
            return ExerciseRead(**exercise.to_dict())

    return ExerciseRead(**exercise.to_dict())


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
    await session.refresh(exercise)

    return ExerciseRead(**exercise.to_dict())


@router.post("/{exercise_id}/test-case", response_model=TestCaseRead)
async def create_test_case(exercise_id: int, new_test_case: TestCaseCreate,
                           session: AsyncSession = Depends(get_session)) -> TestCaseRead:
    test_case = TestCase(exercise_id=exercise_id, **new_test_case.model_dump())
    session.add(test_case)
    await session.commit()

    await session.refresh(test_case)

    return TestCaseRead(**test_case.to_dict())


@router.get("/{exercise_id}/test-case", response_model=list[TestCaseRead], status_code=status.HTTP_200_OK)
async def get_test_cases(exercise_id: int, session: AsyncSession = Depends(get_session)) -> list[TestCaseRead]:
    statement = select(TestCase).where(TestCase.exercise_id == exercise_id)
    result = await session.execute(statement)
    test_cases = result.scalars().all()

    return [TestCaseRead(**case.to_dict()) for case in test_cases]
