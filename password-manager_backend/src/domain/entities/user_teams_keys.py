import uuid
from dataclasses import dataclass
from typing import Optional


@dataclass
class UserTeamsKeys:
    user_id: uuid.UUID
    team_id: uuid.UUID
    team_key_encrypted: str
    id: Optional[uuid.UUID] = None
