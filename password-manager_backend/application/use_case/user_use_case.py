import uuid

from application.dto.user_dto import CreateUserDTO, UpdateUserDTO, UserDTO
from application.exceptions.user_use_Case_exceptions import *
from application.use_case.publisher import EventPublisher
from domain.interfaces.user_service_interface import IUserService
from domain.interfaces.events_mongoDB_interface import IEventsMongoDB


class CreateUserUseCase:
    def __init__(self, UserRepository: IUserService, event_repository: IEventsMongoDB):
        self.user_repository = UserRepository
        self.event_repository = event_repository

    async def execute(self, user_create: CreateUserDTO):
        try:
            user_entity = user_create.to_entity()
            user = self.user_repository.create_user(user_entity)

            if self.event_repository:
                publisher = EventPublisher(self.event_repository)
                publisher.publish(
                    event_type="UserCreated",
                    payload={
                        "user_id": str(user.id),
                        "keycloak_id": str(user_create.id_keycloak),
                    },
                    user_id=uuid.UUID(str(user.id)),
                )

            return user

        except Exception as e:
            raise UserCreationException(str(e)) from e


class GetUserByKeycloakIdUseCase:
    def __init__(self, UserRepository: IUserService):
        self.user_repository = UserRepository

    def execute(self, main_user_id: uuid.UUID) -> UserDTO:
        try:
            user = self.user_repository.get_user_by_keycloak_id(main_user_id)
            return user

        except Exception as e:
            raise UserRetrievalException(str(e)) from e


class UpdateUserByIdUseCase:
    def __init__(self, UserRepository: IUserService, event_repository: IEventsMongoDB):
        self.user_repository = UserRepository
        self.event_repository = event_repository

    async def execute(self, user_id: uuid.UUID, new_user: UpdateUserDTO):
        try:
            existing_user = self.user_repository.get_user_by_keycloak_id(user_id)
            new_user_entity = new_user.to_entity(existing_user=existing_user)
            updated = self.user_repository.update_user_by_id(user_id, new_user_entity)

            if updated and self.event_repository:
                publisher = EventPublisher(self.event_repository)
                publisher.publish(
                    event_type="UserUpdated",
                    payload={
                        "user_id": str(user_id),
                    },
                    user_id=user_id,
                )

            return updated

        except Exception as e:
            raise UserUpdateException(str(e)) from e


class DeleteUserByIdUseCase:
    def __init__(self, user_repository: IUserService, event_repository: IEventsMongoDB):
        self.user_repository = user_repository  
        self.event_repository = event_repository

    async def execute(self, user_id: uuid.UUID):
        try:
            deleted = self.user_repository.delete_user_by_id(user_id)

            if deleted and self.event_repository:
                publisher = EventPublisher(self.event_repository)
                publisher.publish(
                    event_type="UserDeleted",
                    payload={
                        "user_id": str(user_id),
                    },
                    user_id=user_id,
                )

            return deleted

        except Exception as e:
            raise UserDeletionException(str(e)) from e