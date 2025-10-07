import sqlalchemy as sa

from app.db.database import Base


class Tan(Base):
    __tablename__ = "tan"

    code = sa.Column(sa.VARCHAR(29), primary_key=True, nullable=False)
    valid_from = sa.Column(sa.DateTime(timezone=True), nullable=True)
    valid_to = sa.Column(sa.DateTime(timezone=True), nullable=True)
    competition_id = sa.Column(sa.INTEGER, sa.ForeignKey("competition.id"), nullable=True)

    def to_dict(self):
        return {
            "code": self.code,
            "valid_from": self.valid_from,
            "valid_to": self.valid_to,
            "competition_id": self.competition_id
        }
