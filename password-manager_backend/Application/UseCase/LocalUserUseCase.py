import uuid

from Application.DTO.LocalUserDTO import CreateLocalUser, UpdateLocalUser
from Domain.PasswordCripting.PasswordCripting import HashMasterPassword
from Application.Exceptions.LocalUserUseCaseExceptions import *

class CreateLocalUserUseCase():
    def __init__(self, LocalUserRepository):
        self.LocalUserRepository = LocalUserRepository
        
    def execute(self, localuser_create: CreateLocalUser):
        try:
            generated_hash, generated_salt = HashMasterPassword(localuser_create.MasterPassword)
            return self.LocalUserRepository.CreateLocalUser(localuser_create, generated_hash, generated_salt)
        except Exception as e:
            raise LocalUserCreationException(str(e)) from e

class GetAllLocalUsersByMainUserIdUseCase():
    def __init__(self, LocalUserRepository):
        self.LocalUserRepository = LocalUserRepository
        
    def execute(self, mainUserId: uuid.uuid4):
        try:
            return self.LocalUserRepository.GetAllLocalUserById(mainUserId)
        except Exception as e:
            raise LocalUserRetrievalException(str(e)) from e
        
class UpdateLocalUserByIdUseCase():
    def __init__(self, LocalUserRepository):
        self.LocalUserRepository = LocalUserRepository
        
    def execute(self, localUserId: uuid.UUID, new_local_user: UpdateLocalUser):
        try:
            new_generated_hash, new_generated_salt = HashMasterPassword(new_local_user.NewMasterPassword)
            return self.LocalUserRepository.UpdateLocalUserById(localUserId, new_generated_hash, new_generated_salt)
        except Exception as e:
            raise LocalUserUpdateException(str(e)) from e        

class DeleteLocalUserByIdUseCase():
    def __init__(self, LocalUserRepository):
        self.LocalUserRepository = LocalUserRepository
        
    def execute(self, user_id: uuid.UUID):
        try:
            return self.LocalUserRepository.DeleteLocalUserById(user_id)
        except Exception as e:
            raise LocalUserDeletionException(str(e)) from e