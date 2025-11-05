from datetime import datetime, timezone


def get_datetime_now():
    yield datetime.now(timezone.utc)
