import uuid
from dataclasses import dataclass
from typing import Optional


@dataclass
class UserFavorite:
    user_id: uuid.UUID
    sub_account_id: uuid.UUID
    id: Optional[uuid.UUID] = None
