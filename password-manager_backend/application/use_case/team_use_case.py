from typing import Optional
import uuid
from application.use_case.publisher import EventPublisher
from application.dto.team_dto import TeamDTO, CreateTeamDTO, UpdateTeamDTO, DeleteTeamDTO
from application.exceptions.team_use_case_exceptions import *

from domain.interfaces.team_service_interface import ITeamService
from domain.interfaces.events_mongoDB_interface import IEventsMongoDB

class CreateTeamUseCase:
    def __init__(self, TeamRepository: ITeamService, event_repository: IEventsMongoDB):
        self.team_repository = TeamRepository
        self.event_repository = event_repository

    def execute(self, interactor_id: uuid.UUID, team_create: CreateTeamDTO):
        try:
            team_entity = team_create.to_entity()
            team = self.team_repository.CreateTeam(team_entity)

            if self.event_repository:
                publisher = EventPublisher(self.event_repository)
                publisher.publish(
                    event_type="TeamCreated",
                    payload={
                        "team_id": str(team.id),
                        "team_name": team.name,
                        "team_salt": team.salt_argon
                    },
                    user_id=interactor_id
                )
            
            return team
        
        except Exception as e:
            raise TeamCreationException(str(e)) from e
    
class GetTeamByIdUseCase:
    def __init__(self, TeamRepository: ITeamService):
        self.team_repository = TeamRepository

    def execute(self, team_id: uuid.UUID):
        try:
            team = self.team_repository.GetTeamById(team_id)
            return TeamDTO(
                id=uuid.UUID(str(team.id)),
                name=str(team.name),
                salt_argon=str(team.salt_argon)
            )
        
        except Exception as e:
            raise TeamRetrievalByIdException(str(e)) from e
    
class GetTeamsByUserIdUseCase:
    def __init__(self, team_repository: ITeamService):
        self.team_repository = team_repository

    def execute(self, user_id: uuid.UUID):
        try:
            teams = self.team_repository.GetTeamsByUserId(user_id)
            return [TeamDTO(
                id=uuid.UUID(str(team.id)),
                name=str(team.name),
                salt_argon=str(team.salt_argon)
            ) for team in teams]
        
        except Exception as e:
            raise TeamsRetrievalByUserIdException(str(e)) from e
    
class UpdateTeamByIdUseCase:
    def __init__(self, team_repository: ITeamService, event_repository: Optional[IEventsMongoDB] = None):
        self.team_repository = team_repository
        self.event_repository = event_repository

    def execute(self, interactor_id: uuid.UUID, new_team: UpdateTeamDTO):
        try:
            team_entity = new_team.to_entity(self.team_repository.GetTeamById(new_team.id))
            team = self.team_repository.UpdateTeamById(team_entity)

            if self.event_repository:
                publisher = EventPublisher(self.event_repository)
                publisher.publish(
                    event_type="TeamUpdated",
                    payload={
                        "team_id": str(team.id),
                        "team_name": team.name,
                        "team_salt": team.salt_argon
                    },
                    user_id=interactor_id
                )

            return TeamDTO(
                id=uuid.UUID(str(team.id)),
                name=str(team.name),
                salt_argon=str(team.salt_argon)
            )
        
        except Exception as e:
            raise TeamUpdateException(str(e)) from e
    
class DeleteTeamByIdUseCase:    
    def __init__(self, team_repository: ITeamService, event_repository: IEventsMongoDB):
        self.team_repository = team_repository
        self.event_repository = event_repository

    def execute(self, interactor_id: uuid.UUID, team_to_delete: DeleteTeamDTO):
        try:
            self.team_repository.DeleteTeamById(team_to_delete.id)

            if self.event_repository:
                publisher = EventPublisher(self.event_repository)
                publisher.publish(
                    event_type="TeamDeleted",
                    payload={
                        "team_id": str(team_to_delete.id)
                    },
                    user_id=interactor_id
                )

        except Exception as e:
            raise TeamDeleteException(str(e)) from e