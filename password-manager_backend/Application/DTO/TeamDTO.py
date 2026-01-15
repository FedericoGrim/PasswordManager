from uuid import UUID
from pydantic import BaseModel
from typing import Optional

from Domain.Entities.Team import Team

class TeamDTO(BaseModel):
    id: UUID
    salt_argon: str

    def to_entity(self):
        return Team(
            id=self.id,
            salt_argon=self.salt_argon
        )
    
class CreateTeamDTO(BaseModel):
    salt_argon: str

    def to_entity(self):
        return Team(
            salt_argon=self.salt_argon
        )

class UpdateTeamDTO(BaseModel):
    salt_argon: Optional[str]

    def to_entity(self, existing_team: Team):
        return Team(
            id=existing_team.id,
            salt_argon=self.salt_argon if self.salt_argon is not None else existing_team.salt_argon
        )