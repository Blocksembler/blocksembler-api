import datetime
import json
import logging
from uuid import uuid4

import amqp
from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schema.grading import ExerciseSubmission
from app.config import MESSAGE_QUEUE_URL, MESSAGE_QUEUE_PASSWORD, MESSAGE_QUEUE_USER
from app.db.database import get_session
from app.db.model.exercise import ExerciseProgress
from app.db.model.grading import GradingJob

router = APIRouter(
    prefix="/submission",
    tags=["submission"],
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=str)
async def create_submission(new_submission: ExerciseSubmission, session: AsyncSession = Depends(get_session)) -> str:
    stmt = select(ExerciseProgress).where(ExerciseProgress.exercise_id == new_submission.exercise_id,
                                          ExerciseProgress.tan_code == new_submission.tan_code,
                                          ExerciseProgress.end_time.is_(None))
    result = await session.execute(stmt)
    exercise_progress = result.scalars().first()

    if not exercise_progress:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tried to submit for non-active exercise")

    try:
        with amqp.Connection(MESSAGE_QUEUE_URL, userid=MESSAGE_QUEUE_USER, password=MESSAGE_QUEUE_PASSWORD) as c:
            job_msg = {
                "job_id": str(uuid4()),
                "exercise_id": new_submission.exercise_id,
                "tan_code": new_submission.tan_code,
                "solution_code": new_submission.solution_code
            }

            session.add(GradingJob(
                id=job_msg["job_id"],
                tan_code=job_msg["tan_code"],
                exercise_id=job_msg["exercise_id"],
                status="pending",
                started=datetime.datetime.now()
            ))

            ch = c.channel()
            ch.basic_publish(amqp.Message(json.dumps(job_msg)), routing_key='grading_jobs')

            await session.commit()
            return job_msg["job_id"]

    except Exception as e:
        logging.error(e)
        await session.rollback()
        raise HTTPException(status_code=500, detail="Scheduling grading job failed.")
