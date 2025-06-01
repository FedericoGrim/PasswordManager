from sqlalchemy import Column, String, UUID, ForeignKey
import uuid

from Domain.Entities.Base import Base

class SubAccount(Base):
    __tablename__ = "Subaccounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("local_users.Id"), nullable=False)
    title = Column(String(100), nullable=False) 
    username = Column(String(100), nullable=True)
    password_encrypted = Column(String, nullable=False)  
    url = Column(String(255), nullable=True)
