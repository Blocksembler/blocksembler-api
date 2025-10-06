from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.db.database import get_session
from app.main import app

HEALTHY_DB_URI = "sqlite+aiosqlite:///:memory:"
UNHEALTHY_DB_URI = "sqlite+aiosqlite:///file:not-existing.sqlite?mode=rw&uri=true"


class TestHealth:
    def setup_method(self):
        self._engine = create_async_engine(HEALTHY_DB_URI, echo=True, future=True)
        self._unhealthy_engine = create_async_engine(UNHEALTHY_DB_URI,
                                                     echo=True,
                                                     future=True)

    def test_health_when_healthy(self):
        async def get_session_override() -> AsyncSession:
            async with async_sessionmaker(bind=self._engine)() as session:
                yield session

        app.dependency_overrides[get_session] = get_session_override

        client = TestClient(app)
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_unhealth_when_healthy(self):
        async def get_session_override() -> AsyncSession:
            async with async_sessionmaker(bind=self._unhealthy_engine)() as session:
                yield session

        app.dependency_overrides[get_session] = get_session_override

        client = TestClient(app)
        response = client.get("/health")

        assert response.status_code == 500
