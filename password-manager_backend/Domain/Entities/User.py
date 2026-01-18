from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship
import uuid
from Domain.Entities.Base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    id_keycloak = Column(UUID, unique=True, nullable=False, default=uuid.uuid4)