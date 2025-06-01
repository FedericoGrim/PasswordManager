from pydantic import BaseModel
from typing import Optional
from uuid import UUID

from Domain.Entities.LocalUser import LocalUser

class CreateLocalUser(BaseModel):
    IdKeycloak: UUID
    MasterPassword: str

    def to_entity(self, generatedHash, generatedSalt):
        return LocalUser(
            IdKeycloak=self.IdKeycloak,
            HashMasterPassword=generatedHash,
            SaltArgon=generatedSalt,
        )


class UpdateLocalUser(BaseModel):
    NewMasterPassword: Optional[str] = None
    