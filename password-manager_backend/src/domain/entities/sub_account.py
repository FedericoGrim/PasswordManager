import uuid

from sqlalchemy import String, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.entities.base import Base
from domain.entities.team import Team
from domain.entities.team_perm_level import TeamPermLevel

class SubAccount(Base):
    __tablename__ = "sub_accounts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    team_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    username_encrypted: Mapped[str | None] = mapped_column(String(100), nullable=True)
    email_encrypted: Mapped[str | None] = mapped_column(String(255), nullable=True)
    password_encrypted: Mapped[str] = mapped_column(String, nullable=False)
    site_link_encrypted: Mapped[str | None] = mapped_column(String(255), nullable=True)
    required_perm_level_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("team_perm_levels.id", ondelete="CASCADE"), nullable=False)

    Team: Mapped[Team] = relationship("Team", backref="sub_accounts")
    RequiredPermLevel: Mapped[TeamPermLevel] = relationship("TeamPermLevel", backref="sub_accounts")
