from sqlalchemy import Column, String, UUID, ForeignKey
from sqlalchemy.orm import relationship
import uuid

from domain.entities.base import Base

class SubAccount(Base):
    __tablename__ = "sub_accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(100), nullable=False) 
    username = Column(String(100), nullable=True)
    email = Column(String(255), nullable=True)
    password = Column(String, nullable=False)  
    link = Column(String(255), nullable=True)
    necessary_role = Column(String(50), nullable=False)

    Team = relationship("Team", backref="sub_accounts")