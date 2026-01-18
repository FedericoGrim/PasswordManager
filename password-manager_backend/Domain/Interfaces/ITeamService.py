import uuid
from abc import ABC, abstractmethod

from Domain.Entities.Team import Team

@abstractmethod
class ITeamService(ABC):
    @abstractmethod
    def CreateTeam(self, new_team: Team) -> dict:
        pass

    @abstractmethod
    def GetTeamById(self, teamId: uuid.UUID) -> dict:
        pass

    @abstractmethod
    def UpdateTeamById(self, teamId: uuid.UUID, new_team: Team) -> dict:
        pass

    @abstractmethod
    def DeleteTeamById(self, teamId: uuid.UUID) -> dict:
        pass