import uuid
from dataclasses import dataclass
from typing import Optional


@dataclass
class SubAccountCategories:
    sub_account_id: uuid.UUID
    category_id: uuid.UUID
    id: Optional[uuid.UUID] = None
