import sqlalchemy as sa

from app.db.database import Base


class Exercise(Base):
    __tablename__ = "exercise"

    id = sa.Column(sa.INTEGER, default=None, primary_key=True)
    title = sa.Column(sa.TEXT, nullable=False)
    markdown = sa.Column(sa.TEXT, nullable=False)
    coding_mode = sa.Column(sa.VARCHAR(3), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "markdown": self.markdown,
            "coding_mode": self.coding_mode,
        }
