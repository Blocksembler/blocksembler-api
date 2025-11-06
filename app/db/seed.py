import asyncio

from sqlalchemy.ext.asyncio.session import AsyncSession

from app.db.database import async_session_maker, engine, Base
from app.db.model import Tan, Competition, Exercise


async def wipe_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def insert_demo_data():
    async with async_session_maker() as session:
        await wipe_db()

        third_exercise_id = await insert_exercise(session, Exercise(
            title="Third Exercise!",
            markdown="# 🚀 Third Exercise: \n lorem ipsum",
            coding_mode="bbp",
            skip_delay=10
        ))

        second_exercise_id = await insert_exercise(session, Exercise(
            title="Second Exercise!",
            markdown="# 🚀 Second Exercise: \n lorem ipsum",
            coding_mode="bbp",
            skip_delay=10,
            next_exercise_id=third_exercise_id
        ))

        first_exercise_id = await insert_exercise(session, Exercise(
            title="First Exercise!",
            markdown="# 🚀First Exercise: \n lorem ipsum",
            coding_mode="bbp",
            skip_delay=10,
            next_exercise_id=second_exercise_id
        ))

        competition_id = await insert_competition(session, Competition(
            name="test-competition",
            first_exercise_id=first_exercise_id
        ))

        tan_code = await insert_tan(session, Tan(
            code="test-tan",
            competition_id=competition_id
        ))


async def insert_exercise(session: AsyncSession, exercise: Exercise) -> int:
    session.add(exercise)
    await session.commit()
    await session.refresh(exercise)
    return exercise.id


async def insert_competition(session: AsyncSession, competition: Competition) -> int:
    session.add(competition)
    await session.commit()
    await session.refresh(competition)
    return competition.id


async def insert_tan(session: AsyncSession, tan: Tan) -> str:
    session.add(tan)
    await session.commit()
    await session.refresh(tan)
    return tan.code


asyncio.run(insert_demo_data())
