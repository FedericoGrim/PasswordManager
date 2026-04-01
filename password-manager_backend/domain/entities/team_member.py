from sqlalchemy.sql.sqltypes import String, UUID
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy import Column, ForeignKey

from domain.entities.base import Base

class TeamMember(Base):
    __tablename__ = 'team_members'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(50), nullable=False)

    User = relationship("User", backref="team_members")
    Team = relationship("Team", backref="team_members")
