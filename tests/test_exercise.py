import asyncio
import datetime

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from starlette import status

from app.db.database import Base, get_session
from app.db.model import Exercise, Tan
from app.db.model.exercise import ExerciseProgress, Competition
from app.main import app

DB_URI = "sqlite+aiosqlite:///:memory:"

DEMO_COMPETITION = [
    {
        "id": 1,
        "first_exercise_id": 1,
        "name": "Demo Competition",
    }
]

DEMO_TANS = [
    {
        "code": "test-tan-1",
        "competition_id": 1,
        "valid_from": datetime.datetime.now(),
    },
    {
        "code": "test-tan-2",
        "competition_id": 1,
        "valid_from": datetime.datetime.now(),
    },
    {
        "code": "test-tan-3",
        "competition_id": 1,
        "valid_from": datetime.datetime.now(),
    }
]

DEMO_EXERCISES = [
    {
        "id": 1,
        "title": "Demo Exercise 1",
        "markdown": "",
        "coding_mode": "bbp",
        "allow_skip_after": 0,
        "next_exercise_id": 2,
    },
    {
        "id": 2,
        "title": "Demo exercise 2",
        "markdown": "",
        "coding_mode": "bbp",
        "allow_skip_after": 0,
        "next_exercise_id": 3,
    },
    {
        "id": 3,
        "title": "Demo exercise 2",
        "markdown": "",
        "coding_mode": "bbp",
        "allow_skip_after": 0,
        "next_exercise_id": None,
    }
]

DEMO_EXERCISE_PROGRESS = [
    {
        "id": 1,
        "tan_code": "test-tan-1",
        "exercise_id": 1,
        "start_time": datetime.datetime(2025, 10, 7, 18, 30, 0),
        "end_time": datetime.datetime(2025, 10, 7, 19, 30, 0),
        "skipped": False
    },
    {
        "id": 2,
        "tan_code": "test-tan-1",
        "exercise_id": 2,
        "start_time": datetime.datetime(2025, 10, 7, 19, 30, 0),
        "end_time": None,
        "skipped": False
    },
    {
        "id": 3,
        "tan_code": "test-tan-2",
        "exercise_id": 1,
        "start_time": datetime.datetime(2025, 10, 7, 18, 0, 0),
        "end_time": datetime.datetime(2025, 10, 7, 19, 0, 0),
        "skipped": False
    },
    {
        "id": 4,
        "tan_code": "test-tan-2",
        "exercise_id": 2,
        "start_time": datetime.datetime(2025, 10, 7, 19, 0, 0),
        "end_time": datetime.datetime(2025, 10, 7, 20, 0, 0),
        "skipped": False
    },
]


class TestExercise:
    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def insert_exercise(self, exercise: dict) -> None:
        async with self.async_session() as session:
            exercise = Exercise(**exercise)
            session.add(exercise)
            await session.commit()

    async def insert_exercise_progress(self, exercise_progress) -> None:
        async with self.async_session() as session:
            exercise_progress = ExerciseProgress(**exercise_progress)
            session.add(exercise_progress)
            await session.commit()

    async def insert_tan(self, tan) -> None:
        async with self.async_session() as session:
            tan = Tan(**tan)
            session.add(tan)
            await session.commit()

    async def insert_competition(self, competition) -> None:
        async with self.async_session() as session:
            competition = Competition(**competition)
            session.add(competition)
            await session.commit()

    def setup_method(self):
        self.engine = create_async_engine(DB_URI, echo=True, future=True)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

        asyncio.run(self.create_tables())

        for competition in DEMO_COMPETITION:
            asyncio.run(self.insert_competition(competition))

        for tan in DEMO_TANS:
            asyncio.run(self.insert_tan(tan))

        for exercise in DEMO_EXERCISES:
            asyncio.run(self.insert_exercise(exercise))

        for exercise_progress in DEMO_EXERCISE_PROGRESS:
            asyncio.run(self.insert_exercise_progress(exercise_progress))

    def test_get_exercise(self):
        async def get_session_override() -> AsyncSession:
            async with async_sessionmaker(bind=self.engine)() as session:
                yield session

        app.dependency_overrides[get_session] = get_session_override
        client = TestClient(app)

        response = client.get("/exercise/1")

        assert response.json() == DEMO_EXERCISES[0]
        assert response.status_code == 200

    def test_post_exercise(self):
        async def get_session_override() -> AsyncSession:
            async with async_sessionmaker(bind=self.engine)() as session:
                yield session

        app.dependency_overrides[get_session] = get_session_override
        client = TestClient(app)

        new_exercise = {
            "title": "posted exercise",
            "markdown": "",
            "coding_mode": "bbp",
            "allow_skip_after": None,
            "next_exercise_id": None,
        }

        response = client.post("/exercise", json=new_exercise)
        result_exercise = response.json()

        print(result_exercise)

        assert result_exercise["title"] == new_exercise["title"]
        assert result_exercise["markdown"] == new_exercise["markdown"]
        assert result_exercise["coding_mode"] == new_exercise["coding_mode"]
        assert type(result_exercise["id"]) == int
        assert response.status_code == 201

    def test_get_current_exercise(self):
        async def get_session_override() -> AsyncSession:
            async with async_sessionmaker(bind=self.engine)() as session:
                yield session

        app.dependency_overrides[get_session] = get_session_override
        client = TestClient(app)

        response = client.get("/exercise/current", params={"tan_code": "test-tan-1"})

        assert response.status_code == 200
        assert response.json() == DEMO_EXERCISES[1]

    def test_get_current_exercise_with_none_existing_tan(self):
        async def get_session_override() -> AsyncSession:
            async with async_sessionmaker(bind=self.engine)() as session:
                yield session

        app.dependency_overrides[get_session] = get_session_override
        client = TestClient(app)

        response = client.get("/exercise/current", params={"tan_code": "non-existing-tan"})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_current_exercise_with_missing_current_progress_entry_1(self):
        async def get_session_override() -> AsyncSession:
            async with async_sessionmaker(bind=self.engine)() as session:
                yield session

        app.dependency_overrides[get_session] = get_session_override
        client = TestClient(app)

        response = client.get("/exercise/current", params={"tan_code": "test-tan-2"})

        assert response.status_code == 200
        assert response.json() == DEMO_EXERCISES[2]

    def test_get_current_exercise_with_missing_current_progress_entry_2(self):
        async def get_session_override() -> AsyncSession:
            async with async_sessionmaker(bind=self.engine)() as session:
                yield session

        app.dependency_overrides[get_session] = get_session_override
        client = TestClient(app)

        response = client.get("/exercise/current", params={"tan_code": "test-tan-3"})

        assert response.status_code == 200
        assert response.json() == DEMO_EXERCISES[0]
