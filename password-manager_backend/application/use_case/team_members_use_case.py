import uuid

from application.use_case.publisher import EventPublisher
from application.exceptions.team_members_use_case_exceptions import *
from domain.interfaces.team_members_interface import ITeamMembersService
from domain.interfaces.events_mongoDB_interface import IEventsMongoDB

from application.dto.team_members_dto import TeamMembersDTO, CreateTeamMembersDTO, UpdateTeamMembersDTO, RemoveTeamMembersDTO

class AddMemberToTeamUseCase:
    def __init__(self, TeamMembersRepository: ITeamMembersService, event_repository: IEventsMongoDB):
        self.team_members_repository = TeamMembersRepository
        self.event_repository = event_repository

    def execute(self, interactor_id: uuid.UUID, new_member: CreateTeamMembersDTO) -> TeamMembersDTO:
        try:
            team_member = self.team_members_repository.add_member_to_team(new_member.to_entity())

            if self.event_repository:
                publisher = EventPublisher(self.event_repository)
                publisher.publish(
                    event_type="TeamMemberAdded",
                    payload={
                        "member_id": str(team_member.member_id),
                        "team_id": str(team_member.team_id),
                        "role": team_member.role
                    },
                    user_id=interactor_id
                )
            
            return team_member
        
        except Exception as e:
            raise TeamMemberAdditionException(str(e)) from e
        
class GetTeamMemberByIdUseCase:
    def __init__(self, TeamMembersRepository: ITeamMembersService):
        self.team_members_repository = TeamMembersRepository

    def execute(self, member_id: uuid.UUID) -> TeamMembersDTO:
        try:
            member = self.team_members_repository.get_team_member_by_id(member_id)
            return TeamMembersDTO(
                id=uuid.UUID(str(member.id)),
                user_id=uuid.UUID(str(member.user_id)),
                team_id=uuid.UUID(str(member.team_id)),
                role=str(member.role)
            )
        
        except Exception as e:
            raise TeamMemberRetrievalByIdException(str(e)) from e

class GetTeamMembersByTeamIdUseCase:
    def __init__(self, TeamMembersRepository: ITeamMembersService):
        self.team_members_repository = TeamMembersRepository

    def execute(self, team_id: uuid.UUID) -> list[TeamMembersDTO]:
        try:
            team_members = self.team_members_repository.get_members_by_team_id(team_id)
            return [TeamMembersDTO(
            id=uuid.UUID(str(member.id)),
            user_id=uuid.UUID(str(member.user_id)),
            team_id=uuid.UUID(str(member.team_id)),
            role=str(member.role)
        ) for member in team_members]
        
        except Exception as e:
            raise TeamMembersRetrievalByTeamIdException(str(e)) from e

class UpdateTeamMemberRoleUseCase:
    def __init__(self, TeamMembersRepository: ITeamMembersService, event_repository: IEventsMongoDB):
        self.team_members_repository = TeamMembersRepository
        self.event_repository = event_repository

    def execute(self, interactor_id: uuid.UUID, new_user_data: UpdateTeamMembersDTO) -> TeamMembersDTO:
        try:
            updated_member = self.team_members_repository.update_member_role(new_user_data.to_entity(self.team_members_repository.get_team_member_by_id(new_user_data.user_id)))

            if self.event_repository:
                publisher = EventPublisher(self.event_repository)
                publisher.publish(
                    event_type="TeamMemberRoleUpdated",
                    payload={
                        "member_id": str(new_user_data.user_id),
                        "team_id": str(new_user_data.team_id),
                        "new_role": new_user_data.role
                    },
                    user_id=interactor_id
                )
            
            return updated_member
        
        except Exception as e:
            raise TeamMemberRoleUpdateException(str(e)) from e
        
class RemoveMemberFromTeamUseCase:
    def __init__(self, TeamMembersRepository: ITeamMembersService, event_repository: IEventsMongoDB):
        self.team_members_repository = TeamMembersRepository
        self.event_repository = event_repository

    def execute(self, user_interactor: uuid.UUID, user_to_delete: RemoveTeamMembersDTO) -> dict[str, str]:
        try:
            removal_result = self.team_members_repository.remove_member_from_team(
                member_id=user_to_delete.member_id,
                team_id=user_to_delete.team_id
            )

            if self.event_repository:
                publisher = EventPublisher(self.event_repository)
                publisher.publish(
                    event_type="TeamMemberRemoved",
                    payload={
                        "member_id": str(user_to_delete.member_id),
                        "team_id": str(user_to_delete.team_id)
                    },
                    user_id=user_interactor
                )
            
            return removal_result
        
        except Exception as e:
            raise TeamMemberRemovalException(str(e)) from e