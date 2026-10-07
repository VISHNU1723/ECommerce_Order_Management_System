from datetime import datetime, timezone

from sqlalchemy import Column, DateTime


def utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None)


class TimestampMixin:
    created_at = Column(
        DateTime,
        nullable=False,
        default=utcnow
    )

    updated_at = Column(
        DateTime,
        nullable=False,
        default=utcnow,
        onupdate=utcnow
    )