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
