from Application.UseCase.Publisher import EventPublisher

from Application.DTO.TeamDTO import TeamDTO, CreateTeamDTO, UpdateTeamDTO
from Application.Exceptions.TeamUseCase_Exception import *

class CreateTeamUseCase:
    def __init__(self, TeamRepository, EventRepository=None):
        self.TeamRepository = TeamRepository
        self.EventRepository = EventRepository

    def execute(self, team_create: CreateTeamDTO):
        try:
            team_entity = team_create.to_entity()
            team = self.TeamRepository.CreateTeam(team_entity)

            if self.EventRepository:
                publisher = EventPublisher(self.EventRepository)
                publisher.Publish(
                    EventType="TeamCreated",
                    Payload={
                        "team_id": str(team.id),
                        "team_name": team.name,
                        "team_salt": team.salt_argon
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
    def __init__(self, TeamRepository, EventRepository=None):
        self.TeamRepository = TeamRepository
        self.EventRepository = EventRepository

    def execute(self, teamId, team_update: UpdateTeamDTO):
        try:
            team_entity = team_update.to_entity()
            team = self.TeamRepository.UpdateTeamById(teamId, team_entity)

            if self.EventRepository:
                publisher = EventPublisher(self.EventRepository)
                publisher.Publish(
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
    def __init__(self, TeamRepository, EventRepository=None):
        self.TeamRepository = TeamRepository
        self.EventRepository = EventRepository

    def execute(self, teamId):
        try:
            self.TeamRepository.DeleteTeamById(teamId)

            if self.EventRepository:
                publisher = EventPublisher(self.EventRepository)
                publisher.Publish(
                    EventType="TeamDeleted",
                    Payload={
                        "team_id": str(teamId)
                    }
                )

        except Exception as e:
            raise TeamDeleteException(str(e)) from e