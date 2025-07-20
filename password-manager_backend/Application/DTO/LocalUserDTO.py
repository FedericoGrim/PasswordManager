from pydantic import BaseModel
from typing import Optional
from uuid import UUID

from Domain.Entities.LocalUser import LocalUser

class CreateLocalUser(BaseModel):
    """
    DTO for creating a local user.
    This class is used to transfer data for creating a new local user.
    """
    IdKeycloak: UUID
    MasterPassword: str

    def to_entity(self, generatedHash, generatedSalt):
        """
        Converts the DTO to a LocalUser entity.

        Args:
            generatedHash (str): The hash of the master password.
            generatedSalt (str): The salt used for hashing the master password.

        Returns:
            LocalUser: An instance of the LocalUser entity with the provided data.
        """
        return LocalUser(
            IdKeycloak=self.IdKeycloak,
            HashMasterPassword=generatedHash,
            SaltArgon=generatedSalt,
        )


class UpdateLocalUser(BaseModel):
    """
    DTO for updating a local user.
    This class is used to transfer data for updating an existing local user.
    """
    NewMasterPassword: Optional[str] = None
    