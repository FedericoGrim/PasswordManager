import uuid

from Application.DTO.UserDTO import CreateUserDTO
from Application.DTO.TeamDTO import TeamDTO, CreateTeamDTO

from Application.Exceptions.UserUseCaseExceptions import *
from Application.UseCase.Publisher import EventPublisher

class CreateUserUseCase:
    def __init__(self, UserRepository, EventRepository=None, TeamRepository=None, TeamMembersRepository=None):
        self.UserRepository = UserRepository
        self.EventRepository = EventRepository
        self.TeamRepository = TeamRepository
        self.TeamMembersRepository = TeamMembersRepository

    async def execute(self, user_create: CreateUserDTO, salt: bytes):
        try:
            user_entity = user_create.to_entity()
            user = self.UserRepository.CreateUser(
                user_entity
            )
            new_team: CreateTeamDTO = CreateTeamDTO(name="Me", salt_argon=salt.decode() if isinstance(salt, bytes) else salt)
            team_entity = new_team.to_entity()
            team = self.TeamRepository.CreateTeam(team_entity)
            team_members = self.TeamMembersRepository.AddMemberToTeam(member_id=user.id, team_id=team.id, role="owner")
            if self.EventRepository:
                EventPublisher.Publish(
                    EventType="UserCreated",
                    Payload={
                        "user_id": str(user_create.id),
                        "keycloak_id": str(user_create.id_keycloak)
                    }
                )
                EventPublisher.Publish(
                    EventType="TeamCreated",
                    Payload={
                        "team_id": str(team.id),
                        "team_name": team.name,
                        "team_salt": team.salt_argon
                    }
                )
                EventPublisher.Publish(
                    EventType="TeamMemberAdded",
                    Payload={
                        "member_id": str(user.id),
                        "team_id": str(team.id),
                        "role": "owner"
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
                EventPublisher.Publish(
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
                EventPublisher.Publish(
                    EventType="UserDeleted",
                    Payload={
                        "user_id": str(user_id)
                    }
                )

            return deleted
        
        except Exception as e:
            raise UserDeletionException(str(e)) from e
