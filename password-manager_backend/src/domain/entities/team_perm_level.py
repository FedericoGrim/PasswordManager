import uuid
from dataclasses import dataclass
from typing import Optional


@dataclass
class TeamPermLevel:
    team_id: uuid.UUID
    name: str
    rank: int
    id: Optional[uuid.UUID] = None
