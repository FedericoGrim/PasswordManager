import uuid

from sqlalchemy import ForeignKey, UUID, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.entities.base import Base
from domain.entities.user import User
from domain.entities.team import Team
from domain.entities.team_perm_level import TeamPermLevel

class TeamMember(Base):
    __tablename__ = 'team_members'
    __table_args__ = (
        UniqueConstraint('team_id', 'user_id', name='uq_team_members_team_id_user_id'),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    team_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    perm_level_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("team_perm_levels.id", ondelete="CASCADE"), nullable=False)

    User: Mapped[User] = relationship("User", backref="team_members")
    Team: Mapped[Team] = relationship("Team", backref="team_members")
    PermLevel: Mapped[TeamPermLevel] = relationship("TeamPermLevel", backref="team_members")
