import sqlalchemy as sa
from sqlalchemy import ForeignKey

from app.db.database import Base


class LoggingEvent(Base):
    __tablename__ = "logging_event"

    id = sa.Column(sa.INTEGER, primary_key=True, index=True, default=None)
    tan_code = sa.Column(sa.VARCHAR(20), ForeignKey("tan.code"))
    timestamp = sa.Column(sa.DateTime(timezone=True), nullable=True)
    source = sa.Column(sa.TEXT, nullable=True, default=None)
    type = sa.Column(sa.TEXT, nullable=True, default=None)
    payload = sa.Column(sa.JSON)
    exercise_id = sa.Column(sa.INTEGER, sa.ForeignKey("exercise.id"), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "tan_code": self.tan_code,
            "timestamp": self.timestamp,
            "source": self.source,
            "type": self.type,
            "payload": str(self.payload),
            "exercise_id": self.exercise_id,
        }
