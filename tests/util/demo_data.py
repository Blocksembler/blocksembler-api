from datetime import datetime

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
        "valid_from": datetime(2025, 10, 7, 18, 0, 0),
    },
    {
        "code": "test-tan-2",
        "competition_id": 1,
        "valid_from": datetime(2025, 10, 7, 18, 0, 0),
    },
    {
        "code": "test-tan-3",
        "competition_id": 1,
        "valid_from": datetime(2025, 10, 7, 18, 0, 0),
    }
]

EXERCISES = [
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

EXERCISE_PROGRESS_ENTRIES = [
    {
        "id": 1,
        "tan_code": "test-tan-1",
        "exercise_id": 1,
        "start_time": datetime(2025, 10, 7, 18, 30, 0),
        "end_time": datetime(2025, 10, 7, 19, 30, 0),
        "skipped": False
    },
    {
        "id": 2,
        "tan_code": "test-tan-1",
        "exercise_id": 2,
        "start_time": datetime(2025, 10, 7, 19, 30, 0),
        "end_time": None,
        "skipped": False
    },
    {
        "id": 3,
        "tan_code": "test-tan-2",
        "exercise_id": 1,
        "start_time": datetime(2025, 10, 7, 18, 0, 0),
        "end_time": datetime(2025, 10, 7, 19, 0, 0),
        "skipped": False
    },
    {
        "id": 4,
        "tan_code": "test-tan-2",
        "exercise_id": 2,
        "start_time": datetime(2025, 10, 7, 19, 0, 0),
        "end_time": datetime(2025, 10, 7, 20, 0, 0),
        "skipped": False
    },
]

EXERCISE_TEST_CASES = {
    2: [
        {
            "title": "read val to r1 and r2 and store sum in r3 + output",
            "precondition": {
                "registers": {
                    "pc": 0,
                },
                "memory": {}
            },
            "postcondition": {
                "registers": {
                    "r1": 10,
                    "r2": 20,
                    "r3": 30,
                },
                "memory": {}
            },
            "user_input": ["10", "20"],
            "expected_output": ["30"]
        }
    ]
}
