import uuid
from dataclasses import dataclass
from typing import Optional


@dataclass
class Team:
    name: str
    is_personal: bool = False
    id: Optional[uuid.UUID] = None
