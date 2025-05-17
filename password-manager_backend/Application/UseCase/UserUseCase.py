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
        
class UpdateUserUsernameUseCase():
    def __init__(self, UserRepository):
        self.UserRepository = UserRepository
        
    def execute(self, user_id: uuid.UUID, new_username: str):
        try:
            return self.UserRepository.UpdateUserUsername(user_id, new_username)
        except Exception as e:
            raise UserUpdateException(str(e)) from e        

class UpdateUserEmailUseCase():
    def __init__(self, UserRepository):
        self.UserRepository = UserRepository
        
    def execute(self, user_id: uuid.UUID, new_email: str):
        try:
            return self.UserRepository.UpdateUserEmail(user_id, new_email)
        except Exception as e:
            raise UserUpdateException(str(e)) from e

class UpdateUserPasswordUseCase():
    def __init__(self, UserRepository):
        self.UserRepository = UserRepository
        
    def execute(self, user_id: uuid.UUID, new_password: str):
        try:
            generated_hash, generated_salt = HashMasterPassword(new_password)
            return self.UserRepository.UpdateUserPassword(user_id, generated_hash, generated_salt)
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