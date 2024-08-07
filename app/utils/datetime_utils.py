from datetime import datetime, timezone


def aware_utcnow():
    return datetime.now(timezone.utc)
