from sqlalchemy import Column, String, UUID
import uuid
from .Base import Base

class LocalUser(Base):
    __tablename__ = 'local_users'

    Id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    IdKeycloak = Column(UUID, unique=True, nullable=False, default=uuid.uuid4,)
    HashMasterPassword = Column(String, nullable=False)  # colonna per hash password
    SaltArgon = Column(String, nullable=False)           # colonna per salt

    def __repr__(self):
        return f"<LocalUser(IdKeycloak={self.IdKeycloak})>"
