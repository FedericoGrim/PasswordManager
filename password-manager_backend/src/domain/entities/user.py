import uuid
from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    username: str
    code: str
    salt: str
    public_key_ec: bytes
    private_key_ec: bytes
    public_key_pq: bytes
    private_key_pq: bytes
    id: Optional[uuid.UUID] = None
    keycloak_id: Optional[uuid.UUID] = None
