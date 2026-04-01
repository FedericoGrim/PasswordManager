from sqlalchemy import Column, UUID
import uuid
from domain.entities.base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    id_keycloak = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)