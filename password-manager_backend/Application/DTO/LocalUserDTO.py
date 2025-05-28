from pydantic import BaseModel
from typing import Optional
from uuid import UUID

from Domain.Entities.LocalUser import LocalUser

class CreateLocalUser(BaseModel):
    IdKeycloak: UUID
    MasterPassword: str

    def ToEntity(self, generatedHash, generatedSalt, generatedIV):
        return LocalUser(
            IdKeycloak=self.IdKeycloak,
            HashMasterPassword=generatedHash,
            SaltArgon=generatedSalt,
            IV=generatedIV
        )


class UpdateLocalUser(BaseModel):
    NewMasterPassword: Optional[str] = None
    