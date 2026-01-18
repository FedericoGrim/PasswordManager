import uuid
from abc import ABC, abstractmethod

from Domain.Entities.TeamMembers import TeamMembers

@abstractmethod
class ITeamMembersService(ABC):
    @abstractmethod
    def AddMemberToTeam(self, member_id: uuid.UUID, team_id: uuid.UUID, role: str) -> dict:
        pass

    @abstractmethod
    def GetTeamsByMemberId(self, member_id: uuid.UUID) -> list:
        pass

    @abstractmethod
    def GetMembersByTeamId(self, team_id: uuid.UUID) -> list:
        pass

    @abstractmethod
    def UpdateMemberRole(self, member_id: uuid.UUID, team_id: uuid.UUID, new_role: str) -> dict:
        pass

    @abstractmethod
    def RemoveMemberFromTeam(self, member_id: uuid.UUID, team_id: uuid.UUID) -> dict:
        pass