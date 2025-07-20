import uuid
from abc import ABC, abstractmethod

from Domain.Entities.LocalUser import LocalUser

@abstractmethod
class ILocalUserService(ABC):
    @abstractmethod
    def CreateLocalUser(self, user: LocalUser, hash, salt) -> dict:
        """
        Creates a new local user in the database.

        Args:
            user (LocalUser): The local user data to be created.
            hash (str): The hash of the master password.
            salt (str): The salt used for hashing the master password.

        Returns:
            dict: The created local user entity.
        """
        pass

    @abstractmethod
    def GetLocalUserById(self, MainUserId: str) -> dict:
        """
        Retrieves a local users associated with a given Keycloak user ID.

        Args:
            MainUserId (str): The Keycloak user ID to search for.
        
        Returns:
            dict: A list of local users associated with the Keycloak user ID.
        """
        pass

    @abstractmethod
    def UpdateLocalUserById(self, userId: uuid.UUID, newLocalUser: str) -> dict:
        """
        Updates an existing local user by its ID.

        Args:
            userId (uuid.UUID): The ID of the local user to be updated.
            newLocalUser (str): The new local user data to replace the existing one.

        Returns:
            dict: The updated local user entity.
        """
        pass

    @abstractmethod
    def DeleteLocalUserById(self, userId: uuid.UUID) -> dict:
        """
        Deletes a local user by its ID.

        Args:
            userId (uuid.UUID): The ID of the local user to be deleted.

        Returns:
            dict: The result of the deletion operation.
        """
        pass