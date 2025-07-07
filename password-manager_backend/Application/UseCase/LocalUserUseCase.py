import uuid

from Application.DTO.LocalUserDTO import CreateLocalUser, UpdateLocalUser
from Domain.PasswordCripting.PasswordCripting import *
from Application.Exceptions.LocalUserUseCaseExceptions import *

class CreateLocalUserUseCase():
    """
    Use case for creating a local user.
    This class handles the creation of a local user by generating a hash and salt for the master password.
    It interacts with the LocalUserRepository to persist the user data.

    Attributes:
        LocalUserRepository (ILocalUserService): The repository interface for local user operations.
    """
    def __init__(self, LocalUserRepository):
        """
        Initializes the CreateLocalUserUseCase with a LocalUserRepository.
        """
        self.LocalUserRepository = LocalUserRepository
        
    def execute(self, localuser_create: CreateLocalUser):
        """
        Executes the use case to create a local user.
        """
        try:
            generated_hash, generated_salt = HashMasterPassword(localuser_create.MasterPassword)
            return self.LocalUserRepository.CreateLocalUser(localuser_create, generated_hash, generated_salt)
        except Exception as e:
            raise LocalUserCreationException(str(e)) from e

class GetLocalUsersByMainUserIdUseCase():
    """
    Use case for retrieving a local users associated with a main user ID.
    This class interacts with the LocalUserRepository to fetch local users based on the main user ID.

    Attributes:
        LocalUserRepository (ILocalUserService): The repository interface for local user operations.
    """
    def __init__(self, LocalUserRepository):
        """
        Initializes the GetAllLocalUsersByMainUserIdUseCase with a LocalUserRepository.
        """
        self.LocalUserRepository = LocalUserRepository
        
    def execute(self, mainUserId: uuid.uuid4):
        """
        Executes the use case to retrieve all local users by main user ID.
        """
        try:
            return self.LocalUserRepository.GetLocalUserById(mainUserId)
        except Exception as e:
            raise LocalUserRetrievalException(str(e)) from e
        
class UpdateLocalUserByIdUseCase():
    """
    Use case for updating a local user by ID.
    This class handles the update of a local user by generating a new hash for the master password and interacting with the LocalUserRepository to persist the changes.

    Attributes:
        LocalUserRepository (ILocalUserService): The repository interface for local user operations.
    """
    def __init__(self, LocalUserRepository):
        """
        Initializes the UpdateLocalUserByIdUseCase with a LocalUserRepository.
        """
        self.LocalUserRepository = LocalUserRepository
        
    def execute(self, localUserId: uuid.UUID, new_local_user: UpdateLocalUser, salt: str):
        """
        Executes the use case to update a local user by ID.
        """
        try:
            new_generated_hash = hashPassword(new_local_user.NewMasterPassword, salt)
            return self.LocalUserRepository.UpdateLocalUserById(localUserId, new_generated_hash)
        except Exception as e:
            raise LocalUserUpdateException(str(e)) from e        

class DeleteLocalUserByIdUseCase():
    """ 
    Use case for deleting a local user by ID.
    This class handles the deletion of a local user by interacting with the LocalUserRepository.

    Attributes:
        LocalUserRepository (ILocalUserService): The repository interface for local user operations.
    """
    def __init__(self, LocalUserRepository):
        """
        Initializes the DeleteLocalUserByIdUseCase with a LocalUserRepository.
        """
        self.LocalUserRepository = LocalUserRepository
        
    def execute(self, user_id: uuid.UUID):
        """
        Executes the use case to delete a local user by ID.
        """
        try:
            return self.LocalUserRepository.DeleteLocalUserById(user_id)
        except Exception as e:
            raise LocalUserDeletionException(str(e)) from e