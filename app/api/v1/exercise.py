import logging
from datetime import timedelta, datetime, timezone

import sqlalchemy as sa
from fastapi import APIRouter, HTTPException, status, Response
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schema.exercise import ExerciseRead, ExerciseCreate, TestCaseRead, TestCaseCreate, \
    ExerciseWithUnlockTimestamps
from app.db.database import get_session
from app.db.model import Tan
from app.db.model.exercise import Exercise, ExerciseProgress, Competition, TestCase
from app.util import get_datetime_now

router = APIRouter(
    prefix="/exercises",
    tags=["exercises"],
)


@router.get("/current",
            response_model=ExerciseWithUnlockTimestamps,
            status_code=status.HTTP_200_OK)
async def get_current_exercise(tan_code: str, session: AsyncSession = Depends(get_session),
                               now: datetime = Depends(get_datetime_now)) -> ExerciseWithUnlockTimestamps | Response:
    statement = select(Tan).where(Tan.code == tan_code)
    result = await session.execute(statement)
    tan = result.scalars().first()

    if not tan:
        raise HTTPException(status_code=404, detail="TAN code not found")

    statement = (select(Exercise, ExerciseProgress)
                 .join(ExerciseProgress, ExerciseProgress.exercise_id == Exercise.id)
                 .where(sa.and_(ExerciseProgress.tan_code == tan_code,
                                ExerciseProgress.end_time.is_(None))))

    result = await session.execute(statement)
    exercise_and_progress = result.first()

    if not exercise_and_progress:
        stmt = (
            select(Exercise)
            .join(ExerciseProgress, ExerciseProgress.exercise_id == Exercise.id)
            .where(ExerciseProgress.tan_code.like(tan_code))
            .order_by(ExerciseProgress.end_time.desc())
        )

        result = await session.execute(stmt)
        last_exercise = result.scalars().first()

        if last_exercise:
            if last_exercise.next_exercise_id is None:
                return Response(status_code=status.HTTP_204_NO_CONTENT)

            ep = ExerciseProgress(
                tan_code=tan_code,
                exercise_id=last_exercise.next_exercise_id,
                start_time=now,
                skipped=False
            )
            session.add(ep)
            await session.commit()
            await session.refresh(last_exercise)

            stmt = select(Exercise).where(Exercise.id == last_exercise.next_exercise_id)
            result = await session.execute(stmt)
            exercise = result.scalars().first()

            return ExerciseWithUnlockTimestamps(**exercise.to_dict(),
                                                skip_unlock_time=(now + timedelta(minutes=exercise.skip_delay)),
                                                next_grading_allowed_at=now)
        else:
            stmt = (select(Exercise)
                    .join(Competition, Competition.first_exercise_id == Exercise.id)
                    .join(Tan, Tan.competition_id == Competition.id)
                    .where(Tan.code == tan_code))

            result = await session.execute(stmt)
            first_exercise = result.scalars().first()

            ep = ExerciseProgress(
                tan_code=tan_code,
                exercise_id=first_exercise.id,
                start_time=now,
                skipped=False
            )

            session.add(ep)
            await session.commit()

            await session.refresh(first_exercise)

            return ExerciseWithUnlockTimestamps(**first_exercise.to_dict(),
                                                skip_unlock_time=(now + timedelta(minutes=first_exercise.skip_delay)),
                                                next_grading_allowed_at=now)

    exercise, progress = exercise_and_progress

    logging.info(progress.start_time.tzinfo)

    next_grading = progress.next_grading_allowed_at

    if not next_grading:
        next_grading = now

    return ExerciseWithUnlockTimestamps(**exercise.to_dict(),
                                        skip_unlock_time=(
                                                progress.start_time + timedelta(minutes=exercise.skip_delay)),
                                        next_grading_allowed_at=progress.next_grading_allowed_at)


@router.post("/current/skip", status_code=status.HTTP_204_NO_CONTENT)
async def post_skip_current_exercise(tan_code: str, session: AsyncSession = Depends(get_session),
                                     now: datetime = Depends(get_datetime_now)) -> None:
    statement = select(Tan).where(Tan.code == tan_code)
    result = await session.execute(statement)
    tan = result.scalars().first()

    if not tan:
        raise HTTPException(status_code=404, detail="TAN code not found")

    statement = select(ExerciseProgress).where(
        sa.and_(ExerciseProgress.tan_code == tan_code,
                ExerciseProgress.end_time.is_(None)))
    result = await session.execute(statement)
    exercise_progress: ExerciseProgress = result.scalars().first()

    if exercise_progress:
        statement = select(Exercise).where(Exercise.id == exercise_progress.exercise_id)
        result = await session.execute(statement)
        current_exercise: Exercise = result.scalars().first()

        allow_skip_after_date = (exercise_progress.start_time
                                 + timedelta(minutes=current_exercise.skip_delay))

        if allow_skip_after_date.tzinfo is None:
            allow_skip_after_date = allow_skip_after_date.replace(tzinfo=timezone.utc)

        if now < allow_skip_after_date:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Skipping is not allowed before {allow_skip_after_date.isoformat()}.")

        exercise_progress.end_time = now
        exercise_progress.skipped = True

        session.add(exercise_progress)
        await session.commit()
        await session.refresh(exercise_progress)

    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User is not currently working on an exercise.")


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


@router.post("/{exercise_id}/test-cases", response_model=TestCaseRead)
async def create_test_case(exercise_id: int, new_test_case: TestCaseCreate,
                           session: AsyncSession = Depends(get_session)) -> TestCaseRead:
    test_case = TestCase(exercise_id=exercise_id, **new_test_case.model_dump())
    session.add(test_case)
    await session.commit()

    await session.refresh(test_case)

    return TestCaseRead(**test_case.to_dict())


@router.get("/{exercise_id}/test-cases", response_model=list[TestCaseRead], status_code=status.HTTP_200_OK)
async def get_test_cases(exercise_id: int, session: AsyncSession = Depends(get_session)) -> list[TestCaseRead]:
    statement = select(TestCase).where(TestCase.exercise_id == exercise_id)
    result = await session.execute(statement)
    test_cases = result.scalars().all()

    return [TestCaseRead(**case.to_dict()) for case in test_cases]
