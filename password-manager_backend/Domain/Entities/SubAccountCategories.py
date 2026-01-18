from sqlalchemy import Column, String, ForeignKey, UUID
from sqlalchemy.orm import relationship
import uuid

from Domain.Entities.Base import Base
from Domain.Entities.SubAccount import SubAccount
from Domain.Entities.Categories import Categories

class SubAccountCategories(Base):
    __tablename__ = "sub_account_categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    sub_account_id = Column(UUID(as_uuid=True), ForeignKey("sub_accounts.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)

    SubAccount = relationship("SubAccount", backref="sub_account_categories")
    Category = relationship("Categories", backref="sub_account_categories")