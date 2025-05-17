import uuid
from abc import ABC, abstractmethod

from Domain.Objects.UserObj import UserCreate, UserUpdate

@abstractmethod
class IUserService(ABC):
    @abstractmethod
    def CreateUser(self, user: UserCreate, hash, salt) -> dict:
        pass

    @abstractmethod
    def GetUser(self, userEmail: str) -> dict:
        pass

    @abstractmethod
    def UpdateUserUsername(self, userId: uuid.UUID, newUsername: str) -> dict:
        pass

    @abstractmethod
    def UpdateUserEmail(self, userId: uuid.UUID, newEmail: str) -> dict:
        pass

    @abstractmethod
    def UpdateUserPassword(self, userId: uuid.UUID, newPassword: str) -> dict:
        pass

    @abstractmethod
    def DeleteUser(self, userId: uuid.UUID) -> dict:
        pass