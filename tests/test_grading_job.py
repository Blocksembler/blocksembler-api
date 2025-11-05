import asyncio
from unittest.mock import MagicMock, ANY, AsyncMock

from aio_pika.abc import AbstractRobustChannel
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config import GRADING_JOB_ROUTING_KEY
from app.db.database import get_session
from app.main import app
from app.mq.message_queue import get_mq_channel
from tests.util.db_util import create_test_tables, get_override_dependency, insert_demo_data, DB_URI


def setup_mocks():
    channel_mock = MagicMock()
    exchange_mock = MagicMock()
    exchange_mock.publish = AsyncMock()
    channel_mock.get_exchange = AsyncMock(return_value=exchange_mock)
    return channel_mock, exchange_mock


class TestGradingJob:
    def setup_method(self):
        self.engine = create_async_engine(DB_URI, echo=True, future=True)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

        asyncio.run(create_test_tables(self.engine))
        asyncio.run(insert_demo_data(self.async_session))

    def test_post_submission(self):
        channel_mock, exchange_mock = setup_mocks()

        async def get_mq_connection_override() -> AbstractRobustChannel:
            yield channel_mock  # noqa

        app.dependency_overrides[get_session] = get_override_dependency(self.engine)
        app.dependency_overrides[get_mq_channel] = get_mq_connection_override

        client = TestClient(app)

        exercise_submission = {
            "tan_code": "test-tan-1",
            "exercise_id": 2,
            "solution_code": "addi r0 r0 r0"
        }

        response = client.post("/grading-jobs", json=exercise_submission)

        print(response.json())

        assert response.status_code == status.HTTP_201_CREATED
        exchange_mock.publish.assert_awaited_once_with(ANY, routing_key=GRADING_JOB_ROUTING_KEY)

    def test_post_invalid_submission(self):
        channel_mock, exchange_mock = setup_mocks()

        async def get_mq_connection_override() -> AbstractRobustChannel:
            yield channel_mock  # noqa

        app.dependency_overrides[get_session] = get_override_dependency(self.engine)
        app.dependency_overrides[get_mq_channel] = get_mq_connection_override

        client = TestClient(app)

        exercise_submission = {
            "tan_code": "non-existing-tan",
            "exercise_id": 1,
            "solution_code": "addi r0 r0 r0"
        }

        response = client.post("/grading-jobs", json=exercise_submission)

        print(response.json())

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        channel_mock.get_exchange.assert_not_awaited()
        exchange_mock.publish.assert_not_awaited()
