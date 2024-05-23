from sqlalchemy import Column, Integer, String, Enum as SqlEnum
from sqlalchemy.orm import relationship

from core.database.abstract_sql import Base
from core.models.associations import user_team_association, team_admin_association
from core.enums.state import State
from core.enums.brokerage import Brokerage

class TeamOrm(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    office = Column(String(255))
    state = Column(SqlEnum(State))
    brokerage = Column(SqlEnum(Brokerage))

    users = relationship(
        "UserOrm", secondary=user_team_association, back_populates="teams"
    )
    admins = relationship(
        "UserOrm", secondary=team_admin_association
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "users": [
                {"id": user.id, "role": association.role}
                for user, association in zip(self.users, self.user_associations)
            ],
        }
