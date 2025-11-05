import asyncio

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.api.schema.logging_event import LoggingEventRead
from app.db.database import get_session
from app.main import app
from tests.util.db_util import insert_demo_data, DB_URI, create_test_tables, get_override_dependency
from tests.util.demo_data import LOGGING_EVENTS


class TestLoggingEvent:

    def setup_class(self):
        self.engine = create_async_engine(DB_URI, echo=True, future=True)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

        asyncio.run(create_test_tables(self.engine))
        asyncio.run(insert_demo_data(self.async_session))

    def test_get_logging_events(self):
        app.dependency_overrides[get_session] = get_override_dependency(self.engine)
        client = TestClient(app)

        response = client.get("/logging-events/logging-test-tan")

        assert response.status_code == 200
        assert len(response.json()) == 2

        assert response.json()[0] == LoggingEventRead(**LOGGING_EVENTS[0]).model_dump(mode='json')
        assert response.json()[1] == LoggingEventRead(**LOGGING_EVENTS[1]).model_dump(mode='json')



