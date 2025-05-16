import uuid

from Domain.Objects.UserObj import UserCreate, UserUpdate
from Domain.PasswordCripting.PasswordCripting import HashMasterPassword
from Application.Exceptions.UserUseCaseExceptions import *

class CreateUserUseCase():
    def __init__(self, UserRepository):
        self.UserRepository = UserRepository
        
    def execute(self, user_create: UserCreate):
        try:
            generated_hash, generated_salt = HashMasterPassword(user_create.password)
            return self.UserRepository.CreateUser(user_create, generated_hash, generated_salt)
        except Exception as e:
            raise UserCreationException(str(e)) from e

class GetUserByEmailUseCase():
    def __init__(self, UserRepository):
        self.UserRepository = UserRepository
        
    def execute(self, userEmail: str):
        try:
            return self.UserRepository.GetUser(userEmail)
        except Exception as e:
            raise UserRetrievalException(str(e)) from e

class UpdateUserUseCase():
    def __init__(self, UserRepository):
        self.UserRepository = UserRepository
        
    def execute(self, user_id: uuid.UUID, user_update: UserUpdate):
        try:
            return self.UserRepository.UpdateUser(user_id, user_update)
        except Exception as e:
            raise UserUpdateException(str(e)) from e

class DeleteUserUseCase():
    def __init__(self, UserRepository):
        self.UserRepository = UserRepository
        
    def execute(self, user_id: uuid.UUID):
        try:
            return self.UserRepository.DeleteUser(user_id)
        except Exception as e:
            raise UserDeletionException(str(e)) from e