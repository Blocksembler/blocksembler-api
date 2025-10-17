import datetime
import json
import logging
from uuid import uuid4

from aio_pika import Message
from aio_pika.abc import AbstractRobustChannel
from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schema.grading_job import ExerciseSubmission, GradingJobRead
from app.config import MESSAGE_QUEUE_EXCHANGE_NAME
from app.db.database import get_session
from app.db.model.exercise import ExerciseProgress
from app.db.model.grading_job import GradingJob
from app.mq.message_queue import get_mq_channel

router = APIRouter(
    prefix="/grading-jobs",
    tags=["grading jobs"],
)


async def submit_grading_job(job_msg: dict, session: AsyncSession, ch: AbstractRobustChannel):
    session.add(GradingJob(
        id=job_msg["job_id"],
        tan_code=job_msg["tan_code"],
        exercise_id=job_msg["exercise_id"],
        status="pending",
        started=datetime.datetime.now()
    ))

    job_msg["job_id"] = str(job_msg["job_id"])

    exchange = await ch.get_exchange(MESSAGE_QUEUE_EXCHANGE_NAME)
    await exchange.publish(Message(body=json.dumps(job_msg).encode('utf-8')), routing_key='grading_jobs')


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=str)
async def create_submission(new_submission: ExerciseSubmission, session: AsyncSession = Depends(get_session),
                            mq_channel: AbstractRobustChannel = Depends(get_mq_channel)) -> str:
    stmt = select(ExerciseProgress).where(ExerciseProgress.exercise_id == new_submission.exercise_id,
                                          ExerciseProgress.tan_code == new_submission.tan_code,
                                          ExerciseProgress.end_time.is_(None))
    result = await session.execute(stmt)
    exercise_progress = result.scalars().first()

    if not exercise_progress:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tried to submit to an inactive exercise.")

    try:
        job_msg = {
            "job_id": uuid4(),
            "exercise_id": new_submission.exercise_id,
            "tan_code": new_submission.tan_code,
            "solution_code": new_submission.solution_code
        }

        await submit_grading_job(job_msg, session, mq_channel)
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
