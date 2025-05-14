import uuid
from Domain.Objects.UserObj import UserCreate, UserUpdate

class CreateUserUseCase():
    def __init__(self, UserRepository):
        self.UserRepository = UserRepository
        
    def execute(self, user_create: UserCreate):
        try:
            newUser = self.UserRepository.CreateUser(user_create)
            return newUser
        except Exception as e:
            raise e

class GetUserByEmailUseCase():
    def __init__(self, UserRepository):
        self.UserRepository = UserRepository
        
    def execute(self, userEmail: str):
        try:
            user = self.UserRepository.GetUser(userEmail)
            if user:
                return user
            else:
                raise Exception("User not found")
        except Exception as e:
            raise e

class UpdateUserUseCase():
    def __init__(self, UserRepository):
        self.UserRepository = UserRepository
        
    def execute(self, user_id: uuid.UUID, user_update: UserUpdate):
        try:
            updatedUser = self.UserRepository.UpdateUser(user_id, user_update)
            if updatedUser:
                return updatedUser
            else:
                raise Exception("User not found or failed to update")
        except Exception as e:
            raise e

class DeleteUserUseCase():
    def __init__(self, UserRepository):
        self.UserRepository = UserRepository
        
    def execute(self, user_id: uuid.UUID):
        try:
            success = self.UserRepository.DeleteUser(user_id)
            if success:
                return True
            else:
                raise Exception("Failed to delete user")
        except Exception as e:
            raise e