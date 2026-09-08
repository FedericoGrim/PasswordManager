import uuid

from application.exceptions.user_teams_keys_use_case_exceptions import *
from application.dto.user_teams_keys_dto import UserTeamsKeyDTO, CreateUserTeamsKeyDTO, UpdateUserTeamsKeyDTO, RemoveUserTeamsKeyDTO

from domain.interfaces.user_teams_keys_service_interface import IUserTeamsKeysService

class AddUserTeamsKeyUseCase:
    def __init__(self, UserTeamsKeysRepository: IUserTeamsKeysService):
        self.user_teams_keys_repository = UserTeamsKeysRepository

    def execute(self, interactor_id: uuid.UUID, new_key: CreateUserTeamsKeyDTO) -> UserTeamsKeyDTO:
        try:
            user_teams_key = self.user_teams_keys_repository.add_key(new_key.to_entity())

            return UserTeamsKeyDTO(
                id=uuid.UUID(str(user_teams_key.id)),
                user_id=uuid.UUID(str(user_teams_key.user_id)),
                team_id=uuid.UUID(str(user_teams_key.team_id)),
                team_key_encrypted=str(user_teams_key.team_key_encrypted)
            )

        except Exception as e:
            raise UserTeamsKeyAdditionException(str(e)) from e

class GetUserTeamsKeyByIdUseCase:
    def __init__(self, UserTeamsKeysRepository: IUserTeamsKeysService):
        self.user_teams_keys_repository = UserTeamsKeysRepository

    def execute(self, key_id: uuid.UUID) -> UserTeamsKeyDTO:
        try:
            key = self.user_teams_keys_repository.get_key_by_id(key_id)
            return UserTeamsKeyDTO(
                id=uuid.UUID(str(key.id)),
                user_id=uuid.UUID(str(key.user_id)),
                team_id=uuid.UUID(str(key.team_id)),
                team_key_encrypted=str(key.team_key_encrypted)
            )

        except Exception as e:
            raise UserTeamsKeyRetrievalByIdException(str(e)) from e

class GetUserTeamsKeysByTeamIdUseCase:
    def __init__(self, UserTeamsKeysRepository: IUserTeamsKeysService):
        self.user_teams_keys_repository = UserTeamsKeysRepository

    def execute(self, team_id: uuid.UUID) -> list[UserTeamsKeyDTO]:
        try:
            keys = self.user_teams_keys_repository.get_keys_by_team_id(team_id)
            return [UserTeamsKeyDTO(
                id=uuid.UUID(str(key.id)),
                user_id=uuid.UUID(str(key.user_id)),
                team_id=uuid.UUID(str(key.team_id)),
                team_key_encrypted=str(key.team_key_encrypted)
            ) for key in keys]

        except Exception as e:
            raise UserTeamsKeysRetrievalByTeamIdException(str(e)) from e

class GetUserTeamsKeysByUserIdUseCase:
    def __init__(self, UserTeamsKeysRepository: IUserTeamsKeysService):
        self.user_teams_keys_repository = UserTeamsKeysRepository

    def execute(self, user_id: uuid.UUID) -> list[UserTeamsKeyDTO]:
        try:
            keys = self.user_teams_keys_repository.get_keys_by_user_id(user_id)
            return [UserTeamsKeyDTO(
                id=uuid.UUID(str(key.id)),
                user_id=uuid.UUID(str(key.user_id)),
                team_id=uuid.UUID(str(key.team_id)),
                team_key_encrypted=str(key.team_key_encrypted)
            ) for key in keys]

        except Exception as e:
            raise UserTeamsKeysRetrievalByUserIdException(str(e)) from e

class UpdateUserTeamsKeyUseCase:
    def __init__(self, UserTeamsKeysRepository: IUserTeamsKeysService):
        self.user_teams_keys_repository = UserTeamsKeysRepository

    def execute(self, interactor_id: uuid.UUID, new_key_data: UpdateUserTeamsKeyDTO) -> UserTeamsKeyDTO:
        try:
            existing_key = self.user_teams_keys_repository.get_keys_by_user_id(new_key_data.user_id)
            existing_key = next((k for k in existing_key if str(k.team_id) == str(new_key_data.team_id)), None)
            if not existing_key:
                raise Exception("Key not found for this user in this team.")

            updated_key = self.user_teams_keys_repository.update_key(new_key_data.to_entity(existing_key))

            return UserTeamsKeyDTO(
                id=uuid.UUID(str(updated_key.id)),
                user_id=uuid.UUID(str(updated_key.user_id)),
                team_id=uuid.UUID(str(updated_key.team_id)),
                team_key_encrypted=str(updated_key.team_key_encrypted)
            )

        except Exception as e:
            raise UserTeamsKeyUpdateException(str(e)) from e

class RemoveUserTeamsKeyUseCase:
    def __init__(self, UserTeamsKeysRepository: IUserTeamsKeysService):
        self.user_teams_keys_repository = UserTeamsKeysRepository

    def execute(self, interactor_id: uuid.UUID, key_to_delete: RemoveUserTeamsKeyDTO) -> dict[str, str]:
        try:
            removal_result = self.user_teams_keys_repository.remove_key(
                user_id=key_to_delete.user_id,
                team_id=key_to_delete.team_id
            )

            return removal_result

        except Exception as e:
            raise UserTeamsKeyRemovalException(str(e)) from e
