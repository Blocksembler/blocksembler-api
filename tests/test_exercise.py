import asyncio

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.db.database import get_session
from app.main import app
from tests.util.db_util import create_test_tables, get_override_dependency, insert_all_records, DB_URI
from tests.util.demo_data import EXERCISES


class TestExercise:

    def setup_class(self):
        self.engine = create_async_engine(DB_URI, echo=True, future=True)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

        asyncio.run(create_test_tables(self.engine))
        asyncio.run(insert_all_records(self.async_session))

    def test_get_exercise(self):
        app.dependency_overrides[get_session] = get_override_dependency(self.engine)
        client = TestClient(app)

        response = client.get("/exercise/1")

        assert response.json() == EXERCISES[0]
        assert response.status_code == 200

    def test_post_exercise(self):
        app.dependency_overrides[get_session] = get_override_dependency(self.engine)
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
        app.dependency_overrides[get_session] = get_override_dependency(self.engine)
        client = TestClient(app)

        response = client.get("/exercise/current", params={"tan_code": "test-tan-1"})

        assert response.status_code == 200
        assert response.json() == EXERCISES[1]

    def test_get_current_exercise_with_none_existing_tan(self):
        app.dependency_overrides[get_session] = get_override_dependency(self.engine)
        client = TestClient(app)

        response = client.get("/exercise/current", params={"tan_code": "non-existing-tan"})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_current_exercise_with_missing_current_progress_entry_1(self):
        app.dependency_overrides[get_session] = get_override_dependency(self.engine)
        client = TestClient(app)

        response = client.get("/exercise/current", params={"tan_code": "test-tan-2"})

        assert response.status_code == 200
        assert response.json() == EXERCISES[2]

    def test_get_current_exercise_with_missing_current_progress_entry_2(self):
        app.dependency_overrides[get_session] = get_override_dependency(self.engine)
        client = TestClient(app)

        response = client.get("/exercise/current", params={"tan_code": "test-tan-3"})

        assert response.status_code == 200
        assert response.json() == EXERCISES[0]
