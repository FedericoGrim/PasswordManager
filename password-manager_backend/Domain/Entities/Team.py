from sqlalchemy import Column, String, UUID
import uuid

from domain.entities.base import Base

class Team(Base):
    __tablename__ = 'teams'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String, unique=True, nullable=False)
    salt_argon = Column(String, nullable=False)