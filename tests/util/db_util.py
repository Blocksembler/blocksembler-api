from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, async_sessionmaker

from app.db.database import Base
from app.db.model import Exercise, Tan
from app.db.model.exercise import ExerciseProgress, Competition
from tests.util.demo_data import COMPETITIONS, TANS, EXERCISES, EXERCISE_PROGRESS_ENTRIES

DB_URI = "sqlite+aiosqlite:///:memory:"


def get_override_dependency(engine: AsyncEngine):
    async def get_session_override() -> AsyncSession:
        async with async_sessionmaker(bind=engine)() as session:
            yield session

    return get_session_override


async def create_test_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def insert_all_records(session_factory: async_sessionmaker):
    async with session_factory() as session:
        for competition in COMPETITIONS:
            await insert_competition(session, competition)

        for tan in TANS:
            await insert_tan(session, tan)

        for exercise in EXERCISES:
            await insert_exercise(session, exercise)

        for exercise_progress in EXERCISE_PROGRESS_ENTRIES:
            await insert_exercise_progress(session, exercise_progress)


async def insert_exercise(session: AsyncSession, exercise: dict) -> None:
    exercise = Exercise(**exercise)
    session.add(exercise)
    await session.commit()


async def insert_exercise_progress(session: AsyncSession, exercise_progress: dict) -> None:
    exercise_progress = ExerciseProgress(**exercise_progress)
    session.add(exercise_progress)
    await session.commit()


async def insert_tan(session: AsyncSession, tan: dict) -> None:
    tan = Tan(**tan)
    session.add(tan)
    await session.commit()


async def insert_competition(session: AsyncSession, competition: dict) -> None:
    competition = Competition(**competition)
    session.add(competition)
    await session.commit()
