import json
import logging
from datetime import datetime
from uuid import uuid4

import sqlalchemy as sa
from aio_pika import Message
from aio_pika.abc import AbstractRobustChannel
from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schema.grading_job import ExerciseSubmission, GradingJobRead
from app.config import MQ_EXCHANGE_NAME, GRADING_JOB_ROUTING_KEY
from app.db.database import get_session
from app.db.model.exercise import ExerciseProgress
from app.db.model.grading_job import GradingJob
from app.mq.message_queue import get_mq_channel
from app.util import get_datetime_now

INITIAL_JOB_STATUS = "pending"

router = APIRouter(
    prefix="/grading-jobs",
    tags=["grading jobs"],
)


async def submit_grading_job(job_msg: dict, session: AsyncSession, ch: AbstractRobustChannel,
                             now: datetime):
    session.add(GradingJob(
        id=job_msg["job_id"],
        tan_code=job_msg["tan_code"],
        exercise_id=job_msg["exercise_id"],
        status=INITIAL_JOB_STATUS,
        started=now
    ))

    await session.commit()

    job_msg["job_id"] = str(job_msg["job_id"])

    exchange = await ch.get_exchange(MQ_EXCHANGE_NAME)
    await exchange.publish(Message(body=json.dumps(job_msg).encode('utf-8')), routing_key=GRADING_JOB_ROUTING_KEY)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=str)
async def create_submission(new_submission: ExerciseSubmission, session: AsyncSession = Depends(get_session),
                            mq_channel: AbstractRobustChannel = Depends(get_mq_channel),
                            now: datetime = Depends(get_datetime_now)) -> str:
    stmt = select(ExerciseProgress).where(ExerciseProgress.exercise_id == new_submission.exercise_id,
                                          ExerciseProgress.tan_code == new_submission.tan_code,
                                          ExerciseProgress.end_time.is_(None))
    result = await session.execute(stmt)
    exercise_progress = result.scalars().first()

    if not exercise_progress:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tried to submit to an inactive exercise.")

    if exercise_progress.next_grading_allowed_at and exercise_progress.next_grading_allowed_at > now:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                            detail=f"Next grading allowed at {exercise_progress.next_grading_allowed_at}")

    stmt = select(GradingJob).where(sa.and_(GradingJob.exercise_id == new_submission.exercise_id,
                                            GradingJob.tan_code == new_submission.tan_code,
                                            GradingJob.status == INITIAL_JOB_STATUS))

    result = await session.execute(stmt)
    grading_job = result.scalars().first()

    if grading_job:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                            detail="Previous grading job still in progress!")

    try:
        job_msg = {
            "job_id": uuid4(),
            "exercise_id": new_submission.exercise_id,
            "tan_code": new_submission.tan_code,
            "solution_code": new_submission.solution_code
        }

        await submit_grading_job(job_msg, session, mq_channel, now)
        await session.commit()

        return str(job_msg["job_id"])

    except Exception as e:
        logging.error(e)
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Scheduling a grading job failed. {str(e)}")


@router.get("/{job_id}",
            response_model=GradingJobRead,
            status_code=status.HTTP_200_OK)
async def get_submission_status(job_id: str, session: AsyncSession = Depends(get_session)) -> GradingJobRead:
    stmt = select(GradingJob).where(GradingJob.id == job_id)
    result = await session.execute(stmt)
    return GradingJobRead(**result.scalars().first().to_dict())
