from datetime import datetime, timezone
from uuid import uuid4

COMPETITIONS = [
    {
        "id": 1,
        "first_exercise_id": 1,
        "name": "Demo Competition",
    }
]

TANS = [
    {
        "code": "test-tan-1",
        "competition_id": 1,
        "valid_from": datetime(2025, 10, 7, 18, 0, 0, tzinfo=timezone.utc),
    },
    {
        "code": "test-tan-2",
        "competition_id": 1,
        "valid_from": datetime(2025, 10, 7, 18, 0, 0, tzinfo=timezone.utc),
    },
    {
        "code": "test-tan-3",
        "competition_id": 1,
        "valid_from": datetime(2025, 10, 7, 18, 0, 0, tzinfo=timezone.utc),
    },
    {
        "code": "test-tan-4",
        "competition_id": 1,
    },
    {
        "code": "logging-test-tan",
        "competition_id": 1,
        "valid_from": datetime(2025, 10, 7, 18, 0, 0, tzinfo=timezone.utc),
    }
]

LOGGING_EVENTS = [
    {
        "id": 1,
        "tan_code": "logging-test-tan",
        "timestamp": datetime(2025, 10, 7, 18, 0, 1, tzinfo=timezone.utc),
        "source": "button",
        "type": "click",
        "payload": {"msg": "first logging message", "data": [1, 2, 3, 4, 5]},
        "exercise_id": 1
    },
    {
        "id": 2,
        "tan_code": "logging-test-tan",
        "timestamp": datetime(2025, 10, 7, 18, 0, 2, tzinfo=timezone.utc),
        "source": "button",
        "type": "click",
        "payload": {"msg": "second logging message", "data": [5, 4, 3, 2, 1]},
        "exercise_id": 1
    }
]

EXERCISES = [
    {
        "id": 1,
        "title": "Demo Exercise 1",
        "markdown": "",
        "coding_mode": "bbp",
        "skip_delay": 5,
        "next_exercise_id": 2,
    },
    {
        "id": 2,
        "title": "Demo exercise 2",
        "markdown": "",
        "coding_mode": "bbp",
        "skip_delay": 5,
        "next_exercise_id": 3,
    },
    {
        "id": 3,
        "title": "Demo exercise 3",
        "markdown": "",
        "coding_mode": "bbp",
        "skip_delay": 5,
        "next_exercise_id": None,
    }
]

EXERCISE_PROGRESS_ENTRIES = [
    {
        "id": 1,
        "tan_code": "test-tan-1",
        "exercise_id": 1,
        "start_time": datetime(2025, 10, 7, 18, 30, 0, tzinfo=timezone.utc),
        "end_time": datetime(2025, 10, 7, 19, 30, 0, tzinfo=timezone.utc),
        "skipped": False
    },
    {
        "id": 2,
        "tan_code": "test-tan-1",
        "exercise_id": 2,
        "start_time": datetime(2025, 10, 7, 19, 30, 0, tzinfo=timezone.utc),
        "end_time": None,
        "skipped": False,
        "next_grading_allowed_at": datetime(2025, 10, 7, 19, 35, 0, tzinfo=timezone.utc)
    },
    {
        "id": 3,
        "tan_code": "test-tan-2",
        "exercise_id": 1,
        "start_time": datetime(2025, 10, 7, 18, 0, 0, tzinfo=timezone.utc),
        "end_time": datetime(2025, 10, 7, 19, 0, 0, tzinfo=timezone.utc),
        "skipped": False
    },
    {
        "id": 4,
        "tan_code": "test-tan-2",
        "exercise_id": 2,
        "start_time": datetime(2025, 10, 7, 19, 0, 0, tzinfo=timezone.utc),
        "end_time": datetime(2025, 10, 7, 20, 0, 0, tzinfo=timezone.utc),
        "skipped": False
    },
    {
        "id": 5,
        "tan_code": "test-tan-4",
        "exercise_id": 1,
        "start_time": datetime(2025, 10, 7, 19, 0, 0, tzinfo=timezone.utc),
        "end_time": None,
        "skipped": False
    },

]

GRADING_JOBS = [
    {
        "id": uuid4(),
        "tan_code": "test-tan-4",
        "exercise_id": 1,
        "status": "pending",
        "started": datetime(2025, 10, 7, 18, 0, 0, tzinfo=timezone.utc),
    }
]

EXERCISE_TEST_CASES = {
    2: [
        {
            "title": "4 * 5 = 20",
            "precondition": {
                "registers": {
                    "pc": 0
                },
                "memory": {}
            },
            "postcondition": {
                "registers": {
                    "r1": 4,
                    "r2": 5,
                    "r3": 20
                },
                "memory": {}
            },
            "user_input": ["4", "5"],
            "expected_output": ["20"]
        }
    ]
}
