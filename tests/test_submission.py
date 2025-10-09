import asyncio
from unittest.mock import MagicMock, ANY

from amqp import Connection
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config import GRADING_RESPONSE_QUEUE_TTL
from app.db.database import get_session
from app.main import app
from app.mq.message_queue import get_mq_channel
from tests.util.db_util import create_test_tables, get_override_dependency, insert_all_records, DB_URI


class TestSubmission:
    def setup_method(self):
        self.engine = create_async_engine(DB_URI, echo=True, future=True)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

        asyncio.run(create_test_tables(self.engine))
        asyncio.run(insert_all_records(self.async_session))

    def test_post_submission(self):
        mock_channel = MagicMock()

        async def get_mq_connection_override() -> Connection:
            yield mock_channel  # noqa

        app.dependency_overrides[get_session] = get_override_dependency(self.engine)
        app.dependency_overrides[get_mq_channel] = get_mq_connection_override

        client = TestClient(app)

        submission = {
            "tan_code": "test-tan-1",
            "exercise_id": 2,
            "solution_code": "addi r0 r0 r0"
        }

        response = client.post("/submissions", json=submission)

        print(response.json())

        assert response.status_code == status.HTTP_201_CREATED
        mock_channel.basic_publish.assert_called_once_with(ANY, routing_key='grading_jobs')
        mock_channel.queue_declare.assert_called_once_with(queue=ANY, durable=True, arguments={
            "x-expires": GRADING_RESPONSE_QUEUE_TTL,
        })

    def test_post_invalid_submission(self):
        mock_channel = MagicMock()

        async def get_mq_connection_override() -> Connection:
            yield mock_channel  # noqa

        app.dependency_overrides[get_session] = get_override_dependency(self.engine)
        app.dependency_overrides[get_mq_channel] = get_mq_connection_override

        client = TestClient(app)

        submission = {
            "tan_code": "non-existing-tan",
            "exercise_id": 1,
            "solution_code": "addi r0 r0 r0"
        }

        response = client.post("/submissions", json=submission)

        print(response.json())

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        mock_channel.basic_publish.assert_not_called()
        mock_channel.queue_declare.assert_not_called()
