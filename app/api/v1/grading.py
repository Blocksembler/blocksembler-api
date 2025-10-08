import datetime
import json
import logging
from uuid import uuid4

import amqp
from amqp import Connection
from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schema.grading import ExerciseSubmission
from app.config import GRADING_RESPONSE_QUEUE_TTL
from app.db.database import get_session
from app.db.model.exercise import ExerciseProgress
from app.db.model.grading import GradingJob
from app.mq.message_queue import get_mq_connection

router = APIRouter(
    prefix="/submission",
    tags=["submission"],
)


async def submit_grading_job(job_msg: dict, session: AsyncSession, mq_connection: Connection):
    ch = mq_connection.channel()

    ch.queue_declare(queue=f'grading_response.{job_msg["job_id"]}', durable=True, arguments={
        "x-expires": GRADING_RESPONSE_QUEUE_TTL,
    })

    session.add(GradingJob(
        id=job_msg["job_id"],
        tan_code=job_msg["tan_code"],
        exercise_id=job_msg["exercise_id"],
        status="pending",
        started=datetime.datetime.now()
    ))

    job_msg["job_id"] = str(job_msg["job_id"])
    ch.basic_publish(amqp.Message(json.dumps(job_msg)), routing_key='grading_jobs')


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=str)
async def create_submission(new_submission: ExerciseSubmission, session: AsyncSession = Depends(get_session),
                            mq_connection: Connection = Depends(get_mq_connection)) -> str:
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

        await submit_grading_job(job_msg, session, mq_connection)
        await session.commit()

        return str(job_msg["job_id"])

    except Exception as e:
        logging.error(e)
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Scheduling a grading job failed. {str(e)}")
