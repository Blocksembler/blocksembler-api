import asyncio

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.db.database import get_session
from app.main import app
from tests.util.db_util import insert_tan, create_test_tables, get_override_dependency

DB_URI = "sqlite+aiosqlite:///:memory:"


async def insert_test_data(session_factory: async_sessionmaker):
    async with session_factory() as session:
        await insert_tan(session, {"code": "123456"})


class TestTan:
    def setup_method(self):
        self.engine = create_async_engine(DB_URI, echo=True, future=True)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

        asyncio.run(create_test_tables(self.engine))
        asyncio.run(insert_test_data(self.async_session))

    def test_get_tan(self):
        app.dependency_overrides[get_session] = get_override_dependency(self.engine)
        client = TestClient(app)

        response = client.get("/tan/123456")

        assert response.json() == {"code": "123456", "valid_from": None, "valid_to": None}
        assert response.status_code == 200

    def test_get_none_existing_tan(self):
        app.dependency_overrides[get_session] = get_override_dependency(self.engine)
        client = TestClient(app)

        response = client.get("/tan/not-existing-tan")

        assert response.status_code == 404
