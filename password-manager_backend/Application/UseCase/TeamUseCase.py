from Application.UseCase.Publisher import EventPublisher

from Application.DTO.TeamDTO import TeamDTO
from Application.Exceptions.TeamUseCase_Exception import *

class CreateTeamUseCase:
    def __init__(self, TeamRepository, TeamMembersRepository=None):
        self.TeamRepository = TeamRepository
        self.TeamMembersRepository = TeamMembersRepository

    def execute(self, team_create: TeamDTO, user_id=None):
        try:
            team = self.TeamRepository.CreateTeam(team_create)
            team_members = self.TeamMembersRepository.AddMemberToTeam(
                member_id=user_id,
                team_id=team_create.id,
                role="owner"
            )

            if self.TeamMembersRepository and user_id:
                self.TeamMembersRepository.Publish(
                    EventType="TeamMemberAdded",
                    Payload={
                        "member_id": str(user_id),
                        "team_id": str(team_create.id),
                        "role": "owner"
                    }
                )

            if self.TeamRepository:
                self.TeamRepository.Publish(
                    EventType="TeamCreated",
                    Payload={
                        "team_id": str(team_create.id),
                        "team_name": team_create.name,
                        "team_salt": team_create.salt_argon
                    }
                )
            
            return team
        
        except Exception as e:
            raise TeamCreationException(str(e)) from e
    
class GetTeamByIdUseCase:
    def __init__(self, TeamRepository):
        self.TeamRepository = TeamRepository

    def execute(self, teamId):
        try:
            team = self.TeamRepository.GetTeamById(teamId)
            return team
        
        except Exception as e:
            raise TeamRetrievalByIdException(str(e)) from e
    
class GetTeamsByUserIdUseCase:
    def __init__(self, TeamRepository):
        self.TeamRepository = TeamRepository

    def execute(self, userId):
        try:
            teams = self.TeamRepository.GetTeamsByUserId(userId)
            return teams
        
        except Exception as e:
            raise TeamsRetrievalByUserIdException(str(e)) from e
    
class UpdateTeamByIdUseCase:
    def __init__(self, TeamRepository):
        self.TeamRepository = TeamRepository

    def execute(self, teamId, team_update: TeamDTO):
        try:
            team = self.TeamRepository.UpdateTeamById(teamId, team_update)

            if self.TeamRepository:
                self.TeamRepository.Publish(
                    EventType="TeamUpdated",
                    Payload={
                        "team_id": str(teamId),
                        "team_name": team_update.name,
                        "team_salt": team_update.salt_argon
                    }
                )

            return team
        
        except Exception as e:
            raise TeamUpdateException(str(e)) from e
    
class DeleteTeamByIdUseCase:    
    def __init__(self, TeamRepository):
        self.TeamRepository = TeamRepository

    def execute(self, teamId):
        try:
            self.TeamRepository.DeleteTeamById(teamId)

            if self.TeamRepository:
                self.TeamRepository.Publish(
                    EventType="TeamDeleted",
                    Payload={
                        "team_id": str(teamId)
                    }
                )

        except Exception as e:
            raise TeamDeleteException(str(e)) from e