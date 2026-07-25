import uuid

from sqlalchemy import UUID, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from domain.entities.base import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    id_keycloak: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)

    public_key: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    private_key: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
