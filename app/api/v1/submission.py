from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schema.submission import ExerciseSubmission
from app.db.database import get_session
from app.db.model.exercise import ExerciseProgress

router = APIRouter(
    prefix="/submission",
    tags=["submission"],
)


@router.post("/")
async def create_submission(new_submission: ExerciseSubmission, session: AsyncSession = Depends(get_session)) -> int:
    stmt = select(ExerciseProgress).where(ExerciseProgress.exercise_id == new_submission.exercise_id,
                                          ExerciseProgress.tan_code == new_submission.tan_code,
                                          ExerciseProgress.end_time.is_(None))
    result = await session.execute(stmt)
    exercise_progress = result.scalars().first()

    if not exercise_progress:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tried to submit for non-active exercise")

    # TODO: submit new job do RabbitMQ

    return -1
