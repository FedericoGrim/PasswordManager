import uuid

from application.dto.user_dto import CreateUserDTO, UpdateUserDTO, UserDTO
from application.exceptions.user_use_Case_exceptions import *

from domain.interfaces.user_service_interface import IUserService
from domain.interfaces.team_service_interface import ITeamService
from domain.interfaces.team_perm_level_service_interface import ITeamPermLevelService
from domain.interfaces.team_member_service_interface import ITeamMembersService
from domain.entities.team import Team
from domain.entities.team_perm_level import TeamPermLevel
from domain.entities.team_member import TeamMember
from domain.generate_user_code import generate_user_code

PERSONAL_TEAM_OWNER_PERM_LEVEL_NAME = "Owner"
PERSONAL_TEAM_OWNER_PERM_LEVEL_RANK = 0

class CreateUserUseCase:
    def __init__(
        self,
        UserRepository: IUserService,
        TeamRepository: ITeamService,
        TeamPermLevelRepository: ITeamPermLevelService,
        TeamMembersRepository: ITeamMembersService,
    ):
        self.user_repository = UserRepository
        self.team_repository = TeamRepository
        self.team_perm_level_repository = TeamPermLevelRepository
        self.team_members_repository = TeamMembersRepository

    async def execute(self, user_create: CreateUserDTO) -> UserDTO:
        try:
            user_entity = user_create.to_entity()
            user_entity.code = generate_user_code()
            user = self.user_repository.create_user(user_entity)

            personal_team = self.team_repository.CreateTeam(
                Team(name=f"{user.username}#{user.code} Personal Team", is_personal=True)
            )
            owner_perm_level = self.team_perm_level_repository.CreateTeamPermLevel(
                TeamPermLevel(
                    team_id=personal_team.id,
                    name=PERSONAL_TEAM_OWNER_PERM_LEVEL_NAME,
                    rank=PERSONAL_TEAM_OWNER_PERM_LEVEL_RANK,
                )
            )
            self.team_members_repository.add_member_to_team(
                TeamMember(
                    team_id=personal_team.id,
                    user_id=user.id,
                    perm_level_id=owner_perm_level.id,
                )
            )

            return UserDTO.from_entity(user)

        except Exception as e:
            raise UserCreationException(str(e)) from e


class GetUserByKeycloakIdUseCase:
    def __init__(self, UserRepository: IUserService):
        self.user_repository = UserRepository

    def execute(self, main_user_id: uuid.UUID) -> UserDTO:
        try:
            user = self.user_repository.get_user_by_keycloak_id(main_user_id)
            return UserDTO.from_entity(user)

        except Exception as e:
            raise UserRetrievalException(str(e)) from e


class UpdateUserByIdUseCase:
    def __init__(self, UserRepository: IUserService):
        self.user_repository = UserRepository

    async def execute(self, user_id: uuid.UUID, new_user: UpdateUserDTO) -> UserDTO:
        try:
            existing_user = self.user_repository.get_user_by_keycloak_id(user_id)
            new_user_entity = new_user.to_entity(existing_user=existing_user)
            updated = self.user_repository.update_user_by_id(user_id, new_user_entity)

            return UserDTO.from_entity(updated)

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