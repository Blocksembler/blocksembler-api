import asyncio

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.db.database import Base, get_session
from app.db.model import Exercise
from app.main import app

DB_URI = "sqlite+aiosqlite:///:memory:"


class TestExercise:
    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def insert_exercise(self, exercise: dict) -> Exercise:
        async with self.async_session() as session:
            exercise = Exercise(**exercise)
            session.add(exercise)
            await session.commit()

            return exercise

    def setup_method(self):
        self.engine = create_async_engine(DB_URI, echo=True, future=True)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

        self.demo_exercise = {
            "id": 1,
            "title": "Demo Exercise",
            "markdown": "# Exercise header \n \n Exercise Description",
            "coding_mode": "bbp"
        }

        asyncio.run(self.create_tables())
        asyncio.run(self.insert_exercise(self.demo_exercise))

    def test_get_exercise(self):
        async def get_session_override() -> AsyncSession:
            async with async_sessionmaker(bind=self.engine)() as session:
                yield session

        app.dependency_overrides[get_session] = get_session_override
        client = TestClient(app)

        response = client.get("/exercise/1")

        assert response.json() == self.demo_exercise
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
            "coding_mode": "bbp"
        }

        response = client.post("/exercise", json=new_exercise)
        result_exercise = response.json()

        assert result_exercise["title"] == new_exercise["title"]
        assert result_exercise["markdown"] == new_exercise["markdown"]
        assert result_exercise["coding_mode"] == new_exercise["coding_mode"]
        assert type(result_exercise["id"]) == int
        assert response.status_code == 201
