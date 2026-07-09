import uuid

from application.dto.user_dto import CreateUserDTO, UpdateUserDTO, UserDTO
from application.exceptions.user_use_Case_exceptions import *
from domain.interfaces.user_service_interface import IUserService


class CreateUserUseCase:
    def __init__(self, UserRepository: IUserService):
        self.user_repository = UserRepository

    async def execute(self, user_create: CreateUserDTO):
        try:
            user_entity = user_create.to_entity()
            user = self.user_repository.create_user(user_entity)

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
    def __init__(self, UserRepository: IUserService):
        self.user_repository = UserRepository

    async def execute(self, user_id: uuid.UUID, new_user: UpdateUserDTO):
        try:
            existing_user = self.user_repository.get_user_by_keycloak_id(user_id)
            new_user_entity = new_user.to_entity(existing_user=existing_user)
            updated = self.user_repository.update_user_by_id(user_id, new_user_entity)

            return updated

        except Exception as e:
            raise UserUpdateException(str(e)) from e


class DeleteUserByIdUseCase:
    def __init__(self, user_repository: IUserService):
        self.user_repository = user_repository

    async def execute(self, user_id: uuid.UUID):
        try:
            deleted = self.user_repository.delete_user_by_id(user_id)

            return deleted

        except Exception as e:
            raise UserDeletionException(str(e)) from e