import uuid

from Application.DTO.UserDTO import CreateUserDTO, UpdateUserDTO

from Application.Exceptions.UserUseCaseExceptions import *
from Application.UseCase.Publisher import EventPublisher

from Domain.Interfaces.IUserService import IUserService
from Domain.Interfaces.IEventsMongoDB import IEventsMongoDB

class CreateUserUseCase:
    def __init__(self, UserRepository: IUserService, EventRepository: IEventsMongoDB):
        self.UserRepository = UserRepository
        self.EventRepository = EventRepository

    async def execute(self, user_create: CreateUserDTO):
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
                        "user_id": str(user.id),
                        "keycloak_id": str(user_create.id_keycloak)
                    }
                )

            return user
        
        except Exception as e:
            raise UserCreationException(str(e)) from e


class GetUserByKeycloakIdUseCase:
    def __init__(self, UserRepository: IUserService):
        self.UserRepository = UserRepository

    def execute(self, mainUserId: uuid.UUID):
        try:
            return self.UserRepository.GetUserByKeycloakId(mainUserId)
        
        except Exception as e:
            raise UserRetrievalException(str(e)) from e


class UpdateUserByIdUseCase:
    def __init__(self, UserRepository: IUserService, EventRepository: IEventsMongoDB):
        self.UserRepository = UserRepository
        self.EventRepository = EventRepository

    async def execute(self, UserId: uuid.UUID, new_user: UpdateUserDTO):
        try:
            new_user_entity = new_user.to_entity(existing_user=self.UserRepository.GetUserByKeycloakId(UserId))
            updated = self.UserRepository.UpdateUserById(UserId, new_user_entity)
            if updated and self.EventRepository:
                publisher = EventPublisher(self.EventRepository)
                publisher.Publish(
                    EventType="UserUpdated",
                    Payload={
                        "user_id": str(UserId),
                    }
                )

            return updated
        
        except Exception as e:
            raise UserUpdateException(str(e)) from e


class DeleteUserByIdUseCase:
    def __init__(self, UserRepository: IUserService, EventRepository: IEventsMongoDB):
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
