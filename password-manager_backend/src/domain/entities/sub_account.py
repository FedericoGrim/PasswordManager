import uuid
from dataclasses import dataclass
from typing import Optional


@dataclass
class SubAccount:
    """Pure business object: no SQLAlchemy, no knowledge of how it's persisted."""

    team_id: uuid.UUID
    password_encrypted: str
    required_perm_level_id: uuid.UUID
    username_encrypted: Optional[str] = None
    email_encrypted: Optional[str] = None
    site_link_encrypted: Optional[str] = None
    id: Optional[uuid.UUID] = None
