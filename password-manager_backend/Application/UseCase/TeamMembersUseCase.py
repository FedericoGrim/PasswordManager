from Application.UseCase.Publisher import EventPublisher

from Application.Exceptions.TeamMembersUseCase_Exceptions import *

class AddMemberToTeamUseCase:
    def __init__(self, TeamMembersRepository, EventRepository=None):
        self.TeamMembersRepository = TeamMembersRepository
        self.EventRepository = EventRepository

    def execute(self, member_id, team_id, role):
        try:
            team_member = self.TeamMembersRepository.AddMemberToTeam(
                member_id=member_id,
                team_id=team_id,
                role=role
            )

            if self.EventRepository:
                publisher = EventPublisher(self.EventRepository)
                publisher.Publish(
                    EventType="TeamMemberAdded",
                    Payload={
                        "member_id": str(member_id),
                        "team_id": str(team_id),
                        "role": role
                    }
                )
            
            return team_member
        
        except Exception as e:
            raise TeamMemberAdditionException(str(e)) from e
        
class GetTeamMembersByTeamIdUseCase:
    def __init__(self, TeamMembersRepository):
        self.TeamMembersRepository = TeamMembersRepository

    def execute(self, team_id):
        try:
            team_members = self.TeamMembersRepository.GetMembersByTeamId(team_id)
            return team_members
        
        except Exception as e:
            raise TeamMembersRetrievalByTeamIdException(str(e)) from e
        
class GetTeamsByMemberIdUseCase:
    def __init__(self, TeamMembersRepository):
        self.TeamMembersRepository = TeamMembersRepository

    def execute(self, member_id):
        try:
            teams = self.TeamMembersRepository.GetTeamsByMemberId(member_id)
            return teams
        
        except Exception as e:
            raise TeamsRetrievalByMemberIdException(str(e)) from e
        
class UpdateTeamMemberRoleUseCase:
    def __init__(self, TeamMembersRepository, EventRepository=None):
        self.TeamMembersRepository = TeamMembersRepository
        self.EventRepository = EventRepository

    def execute(self, member_id, team_id, new_role):
        try:
            updated_member = self.TeamMembersRepository.UpdateTeamMemberRole(
                member_id=member_id,
                team_id=team_id,
                new_role=new_role
            )

            if self.EventRepository:
                publisher = EventPublisher(self.EventRepository)
                publisher.Publish(
                    EventType="TeamMemberRoleUpdated",
                    Payload={
                        "member_id": str(member_id),
                        "team_id": str(team_id),
                        "new_role": new_role
                    }
                )
            
            return updated_member
        
        except Exception as e:
            raise TeamMemberRoleUpdateException(str(e)) from e
        
class RemoveMemberFromTeamUseCase:
    def __init__(self, TeamMembersRepository, EventRepository=None):
        self.TeamMembersRepository = TeamMembersRepository
        self.EventRepository = EventRepository

    def execute(self, member_id, team_id):
        try:
            removal_result = self.TeamMembersRepository.RemoveMemberFromTeam(
                member_id=member_id,
                team_id=team_id
            )

            if self.EventRepository:
                publisher = EventPublisher(self.EventRepository)
                publisher.Publish(
                    EventType="TeamMemberRemoved",
                    Payload={
                        "member_id": str(member_id),
                        "team_id": str(team_id)
                    }
                )
            
            return removal_result
        
        except Exception as e:
            raise TeamMemberRemovalException(str(e)) from e