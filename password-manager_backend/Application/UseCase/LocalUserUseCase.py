import uuid

from Application.DTO.LocalUserDTO import CreateLocalUser, UpdateLocalUser
from Domain.PasswordCripting.PasswordCripting import HashMasterPassword
from Application.Exceptions.UserUseCaseExceptions import *

class CreateLocalUserUseCase():
    def __init__(self, LocalUserRepository):
        self.LocalUserRepository = LocalUserRepository
        
    def execute(self, localuser_create: CreateLocalUser):
        try:
            generated_hash, generated_salt = HashMasterPassword(localuser_create.MasterPassword)
            return self.LocalUserRepository.CreateLocalUser(localuser_create, generated_hash, generated_salt)
        except Exception as e:
            raise UserCreationException(str(e)) from e

class GetAllLocalUsersByMainUserIdUseCase():
    def __init__(self, LocalUserRepository):
        self.LocalUserRepository = LocalUserRepository
        
    def execute(self, mainUserId: uuid.uuid4):
        try:
            return self.LocalUserRepository.GetAllUsersByMainUserId(mainUserId)
        except Exception as e:
            raise UserRetrievalException(str(e)) from e
        
class UpdateLocalUserByIdUseCase():
    def __init__(self, LocalUserRepository):
        self.LocalUserRepository = LocalUserRepository
        
    def execute(self, user_id: uuid.UUID, new_username: str):
        try:
            return self.LocalUserRepository.UpdateLocalUserByIdUseCase(user_id, new_username)
        except Exception as e:
            raise UserUpdateException(str(e)) from e        

class DeleteLocalUserByIdUseCase():
    def __init__(self, LocalUserRepository):
        self.LocalUserRepository = LocalUserRepository
        
    def execute(self, user_id: uuid.UUID):
        try:
            return self.LocalUserRepository.DeleteUser(user_id)
        except Exception as e:
            raise UserDeletionException(str(e)) from e