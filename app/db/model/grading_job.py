import sqlalchemy as sa

from app.db.database import Base


class GradingJob(Base):
    __tablename__ = "grading_job"

    id = sa.Column(sa.UUID, primary_key=True)
    tan_code = sa.Column(sa.VARCHAR(20), sa.ForeignKey("tan.code"))
    exercise_id = sa.Column(sa.INTEGER, sa.ForeignKey("exercise.id"))
    status = sa.Column(sa.VARCHAR(20))
    started = sa.Column(sa.DateTime(timezone=True))
    terminated = sa.Column(sa.DateTime(timezone=True), nullable=True)
    passed = sa.Column(sa.BOOLEAN, nullable=True)
    feedback = sa.Column(sa.JSON, nullable=True)

    def to_dict(self):
        return {
            "id": str(self.id),
            "tan_code": self.tan_code,
            "exercise_id": self.exercise_id,
            "status": self.status,
            "started": self.started,
            "terminated": self.terminated,
            "passed": self.passed,
            "feedback": self.feedback
        }
