import uuid

from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.entities.base import Base
from domain.entities.sub_account import SubAccount
from domain.entities.categories import Categories

class SubAccountCategories(Base):
    __tablename__ = "sub_account_categories"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    sub_account_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sub_accounts.id", ondelete="CASCADE"), nullable=False)
    category_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)

    SubAccount: Mapped[SubAccount] = relationship("SubAccount", backref="sub_account_categories")
    Category: Mapped[Categories] = relationship("Categories", backref="sub_account_categories")
