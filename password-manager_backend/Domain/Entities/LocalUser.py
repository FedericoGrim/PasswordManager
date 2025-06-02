from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship
import uuid
from Domain.Entities.Base import Base

class LocalUser(Base):
    __tablename__ = 'local_users'

    Id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    IdKeycloak = Column(UUID, unique=True, nullable=False, default=uuid.uuid4)
    HashMasterPassword = Column(String, nullable=False)
    SaltArgon = Column(String, nullable=False)

    SubAccounts = relationship(
        "SubAccount",
        backref="LocalUser",
        cascade="all, delete-orphan",
        passive_deletes=True
    )