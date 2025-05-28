from sqlalchemy import Column, String, UUID
import uuid
from .Base import Base

class LocalUser(Base):
    __tablename__ = 'local_users'

    Id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    IdKeycloak = Column(String, unique=True, nullable=False)
    Username = Column(String, nullable=False)
    Email = Column(String, nullable=False)

    def __repr__(self):
        return f"<LocalUser(IdKeycloak={self.IdKeycloak})>"
