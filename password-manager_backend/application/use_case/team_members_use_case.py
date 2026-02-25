import uuid

from application.use_case.publisher import EventPublisher
from application.exceptions.team_members_use_case_exceptions import *
from domain.interfaces.team_members_interface import ITeamMembersService
from domain.interfaces.events_mongoDB_interface import IEventsMongoDB

from application.dto.team_members_dto import TeamMembersDTO, UpdateTeamMembersDTO

class AddMemberToTeamUseCase:
    def __init__(self, TeamMembersRepository: ITeamMembersService, event_repository: IEventsMongoDB):
        self.team_members_repository = TeamMembersRepository
        self.event_repository = event_repository

    def execute(self, user_interactor: uuid.UUID, user_id: uuid.UUID, new_data: UpdateTeamMembersDTO) -> TeamMembersDTO:
        try:
            existing_member = self.team_members_repository.get_members_by_team_id(user_id)
            new_data_entity = new_data.to_entity(existing_member = existing_member)
            team_member = self.team_members_repository.add_member_to_team(member_id=new_data.member_id, team_id=new_data.team_id, role=new_data.role)

            if self.event_repository:
                publisher = EventPublisher(self.event_repository)
                publisher.publish(
                    event_type="TeamMemberAdded",
                    payload={
                        "member_id": str(member_id),
                        "team_id": str(team_id),
                        "role": role
                    },
                    user_id=user_interactor
                )
            
            return team_member
        
        except Exception as e:
            raise TeamMemberAdditionException(str(e)) from e

class GetTeamMembersByTeamIdUseCase:
    def __init__(self, TeamMembersRepository: ITeamMembersService):
        self.team_members_repository = TeamMembersRepository

    def execute(self, team_id: uuid.UUID) -> list[TeamMembersDTO]:
        try:
            team_members = self.team_members_repository.get_members_by_team_id(team_id)
            return team_members
        
        except Exception as e:
            raise TeamMembersRetrievalByTeamIdException(str(e)) from e

class UpdateTeamMemberRoleUseCase:
    def __init__(self, TeamMembersRepository: ITeamMembersService, event_repository: IEventsMongoDB):
        self.team_members_repository = TeamMembersRepository
        self.event_repository = event_repository

    def execute(self, user_interactor: uuid.UUID, member_id: uuid.UUID, team_id: uuid.UUID, new_role: str):
        try:
            updated_member = self.team_members_repository.update_member_role(
                member_id=member_id,
                team_id=team_id,
                new_role=new_role
            )

            if self.event_repository:
                publisher = EventPublisher(self.event_repository)
                publisher.publish(
                    event_type="TeamMemberRoleUpdated",
                    payload={
                        "member_id": str(member_id),
                        "team_id": str(team_id),
                        "new_role": new_role
                    },
                    user_id=user_interactor
                )
            
            return updated_member
        
        except Exception as e:
            raise TeamMemberRoleUpdateException(str(e)) from e
        
class RemoveMemberFromTeamUseCase:
    def __init__(self, TeamMembersRepository: ITeamMembersService, event_repository: IEventsMongoDB):
        self.team_members_repository = TeamMembersRepository
        self.event_repository = event_repository

    def execute(self, user_interactor: uuid.UUID, member_id: uuid.UUID, team_id: uuid.UUID):
        try:
            removal_result = self.team_members_repository.remove_member_from_team(
                member_id=member_id,
                team_id=team_id
            )

            if self.event_repository:
                publisher = EventPublisher(self.event_repository)
                publisher.publish(
                    event_type="TeamMemberRemoved",
                    payload={
                        "member_id": str(member_id),
                        "team_id": str(team_id)
                    },
                    user_id=user_interactor
                )
            
            return removal_result
        
        except Exception as e:
            raise TeamMemberRemovalException(str(e)) from e