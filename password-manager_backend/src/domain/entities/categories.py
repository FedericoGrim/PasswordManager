import uuid
from dataclasses import dataclass
from typing import Optional


@dataclass
class Categories:
    team_id: Optional[uuid.UUID] = None
    name: Optional[str] = None
    id: Optional[uuid.UUID] = None
