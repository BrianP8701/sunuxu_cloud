from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from core.database.abstract_sql import Base
from core.models.associations import user_team_association  # Import the association table

class TeamOrm(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    users = relationship(
        "UserOrm", secondary=user_team_association, back_populates="teams"
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
