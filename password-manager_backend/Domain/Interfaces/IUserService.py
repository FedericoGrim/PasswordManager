import uuid
from abc import ABC, abstractmethod

from Domain.Entities.User import User

@abstractmethod
class IUserService(ABC):
    @abstractmethod
    def CreateUser(self, user: User) -> dict:
        pass

    @abstractmethod
    def GetUserByKeycloakId(self, user_keycloak_id: str) -> dict:
        pass

    @abstractmethod
    def UpdateUserById(self, user_id: uuid.UUID, new_user: str) -> dict:
        pass

    @abstractmethod
    def DeleteUserById(self, user_id: uuid.UUID) -> dict:
        pass