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
    def UpdateUser(self, userId: uuid.UUID, user: UserUpdate) -> dict:
        pass

    @abstractmethod
    def DeleteUser(self, userId: uuid.UUID) -> dict:
        pass