import uuid

from Application.DTO.UserDTO import UserDTO

from Application.Exceptions.UserUseCaseExceptions import *
from Application.UseCase.Publisher import EventPublisher

class CreateUserUseCase:
    def __init__(self, UserRepository, EventRepository=None):
        self.UserRepository = UserRepository
        self.EventRepository = EventRepository

    async def execute(self, user_create: UserDTO):
        try:
            user_entity = user_create.to_entity()
            user = self.UserRepository.CreateUser(
                user_entity
            )

            if self.EventRepository:
                publisher = EventPublisher(self.EventRepository)
                publisher.Publish(
                    EventType="UserCreated",
                    Payload={
                        "user_id": str(user_create.id),
                        "keycloak_id": str(user_create.id_keycloak)
                    }
                )

            return user
        
        except Exception as e:
            raise UserCreationException(str(e)) from e


class GetUsersByKeycloakIdUseCase:
    def __init__(self, UserRepository):
        self.UserRepository = UserRepository

    def execute(self, mainUserId: uuid.UUID):
        try:
            return self.UserRepository.GetUserById(mainUserId)
        
        except Exception as e:
            raise UserRetrievalException(str(e)) from e


class UpdateUserByIdUseCase:
    def __init__(self, UserRepository, EventRepository=None):
        self.UserRepository = UserRepository
        self.EventRepository = EventRepository

    async def execute(self, UserId: uuid.UUID, newSalt: bytes):
        try:
            updated = self.UserRepository.UpdateUserById(UserId, newSalt)
            if updated and self.EventRepository:
                publisher = EventPublisher(self.EventRepository)
                publisher.Publish(
                    EventType="UserUpdated",
                    Payload={
                        "user_id": str(UserId),
                        "new_salt": newSalt.decode()
                    }
                )

            return updated
        
        except Exception as e:
            raise UserUpdateException(str(e)) from e


class DeleteUserByIdUseCase:
    def __init__(self, UserRepository, EventRepository=None):
        self.UserRepository = UserRepository
        self.EventRepository = EventRepository

    async def execute(self, user_id: uuid.UUID):
        try:
            deleted = self.UserRepository.DeleteUserById(user_id)
            if deleted and self.EventRepository:
                publisher = EventPublisher(self.EventRepository)
                publisher.Publish(
                    EventType="UserDeleted",
                    Payload={
                        "user_id": str(user_id)
                    }
                )

            return deleted
        
        except Exception as e:
            raise UserDeletionException(str(e)) from e
