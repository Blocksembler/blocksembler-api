import asyncio

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.db.database import Base, get_session
from app.db.model import Tan
from app.main import app

DB_URI = "sqlite+aiosqlite:///:memory:"


class TestTan:
    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def insert_tan(self, code: str) -> Tan:
        async with self.async_session() as session:
            tan = Tan(code=code)
            session.add(tan)
            await session.commit()
            return tan

    def setup_method(self):
        self.engine = create_async_engine(DB_URI, echo=True, future=True)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

        asyncio.run(self.create_tables())
        asyncio.run(self.insert_tan("123456"))

    def test_get_tan(self):
        async def get_session_override() -> AsyncSession:
            async with async_sessionmaker(bind=self.engine)() as session:
                yield session

        app.dependency_overrides[get_session] = get_session_override
        client = TestClient(app)

        response = client.get("/tan/123456")

        assert response.json() == {"code": "123456", "valid_from": None, "valid_to": None}
        assert response.status_code == 200

    def test_get_none_existing_tan(self):
        async def get_session_override() -> AsyncSession:
            async with async_sessionmaker(bind=self.engine)() as session:
                yield session

        app.dependency_overrides[get_session] = get_session_override
        client = TestClient(app)

        response = client.get("/tan/not-existing-tan")

        assert response.status_code == 404
