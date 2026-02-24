import uuid
from abc import ABC, abstractmethod

from Domain.Entities.User import User

@abstractmethod
class IUserService(ABC):
    @abstractmethod
    def CreateUser(self, new_user: User) -> User:
        pass

    @abstractmethod
    def GetUserByKeycloakId(self, keycloak_user_id: uuid.UUID) -> User:
        pass

    @abstractmethod
    def UpdateUserById(self, user_id: uuid.UUID, new_user: User) -> User:
        pass

    @abstractmethod
    def DeleteUserById(self, user_id: uuid.UUID) -> dict[str, str]:
        pass