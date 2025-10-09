import sqlalchemy as sa

from app.db.database import Base


class Exercise(Base):
    __tablename__ = "exercise"

    id = sa.Column(sa.INTEGER, default=None, primary_key=True)
    title = sa.Column(sa.TEXT, nullable=False)
    markdown = sa.Column(sa.TEXT, nullable=False)
    coding_mode = sa.Column(sa.VARCHAR(3), nullable=False)
    next_exercise_id = sa.Column(sa.Integer, sa.ForeignKey("exercise.id"), nullable=True)
    allow_skip_after = sa.Column(sa.Integer, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "markdown": self.markdown,
            "coding_mode": self.coding_mode,
            "next_exercise_id": self.next_exercise_id,
            "allow_skip_after": self.allow_skip_after,
        }


class TestCase(Base):
    __tablename__ = "test_case"

    id = sa.Column(sa.INTEGER, default=None, primary_key=True)
    exercise_id = sa.Column(sa.INTEGER, sa.ForeignKey("exercise.id"), nullable=False)
    title = sa.Column(sa.TEXT, nullable=False)
    precondition = sa.Column(sa.JSON, nullable=False)
    postcondition = sa.Column(sa.JSON, nullable=False)
    user_input = sa.Column(sa.JSON, nullable=False)
    expected_output = sa.Column(sa.JSON, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "exercise_id": self.exercise_id,
            "title": self.title,
            "precondition": self.precondition,
            "postcondition": self.postcondition,
            "user_input": self.user_input,
            "expected_output": self.expected_output,
        }


class ExerciseProgress(Base):
    __tablename__ = "exercise_progress"
    __table_args__ = (
        sa.UniqueConstraint("tan_code", "end_time", name="unique_tan_code_and_end_time"),
    )

    id = sa.Column(sa.INTEGER, default=None, primary_key=True)
    tan_code = sa.Column(sa.VARCHAR(20), sa.ForeignKey("tan.code"), nullable=False)
    exercise_id = sa.Column(sa.INTEGER, sa.ForeignKey("exercise.id"), nullable=False)
    start_time = sa.Column(sa.DateTime(timezone=True), nullable=False)
    end_time = sa.Column(sa.DateTime(timezone=True), nullable=True)
    skipped = sa.Column(sa.BOOLEAN, nullable=False)


class Competition(Base):
    __tablename__ = "competition"

    id = sa.Column(sa.INTEGER, default=None, primary_key=True)
    name = sa.Column(sa.TEXT, nullable=False)
    start_time = sa.Column(sa.DateTime(timezone=True), nullable=True)
    end_time = sa.Column(sa.DateTime(timezone=True), nullable=True)
    first_exercise_id = sa.Column(sa.INTEGER, sa.ForeignKey("exercise.id"), nullable=False)
