import uuid
from dataclasses import dataclass
from typing import Optional


@dataclass
class TeamMember:
    team_id: uuid.UUID
    user_id: uuid.UUID
    perm_level_id: uuid.UUID
    id: Optional[uuid.UUID] = None
