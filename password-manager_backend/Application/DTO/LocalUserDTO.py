from pydantic import BaseModel
from typing import Optional
from uuid import UUID

from Domain.Entities.LocalUser import LocalUser

class CreateLocalUserDTO(BaseModel):
    """
    DTO for creating a local user.
    This class is used to transfer data for creating a new local user.
    """
    IdKeycloak: UUID
    Id: UUID
    Salt: str

    def to_entity(self, generatedSalt):
        """
        Converts the DTO to a LocalUser entity.

        Args:
            generatedSalt (str): The salt used for hashing the master password.

        Returns:
            LocalUser: An instance of the LocalUser entity with the provided data.
        """
        return LocalUser(
            IdKeycloak=self.IdKeycloak,
            SaltArgon=generatedSalt,
        )