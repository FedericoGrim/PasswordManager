from uuid import UUID
from pydantic import BaseModel
from typing import Optional

from domain.entities.team import Team

class TeamDTO(BaseModel):
    id: UUID
    name: str
    salt_argon: str

    def to_entity(self):
        return Team(
            id=self.id,
            salt_argon=self.salt_argon
        )
    
class CreateTeamDTO(BaseModel):
    name: str
    salt_argon: str

    def to_entity(self):
        return Team(
            name=self.name,
            salt_argon=self.salt_argon
        )

class UpdateTeamDTO(BaseModel):
    id: UUID
    name: Optional[str]
    salt_argon: Optional[str]

    def to_entity(self, existing_team: Team):
        return Team(
            id=existing_team.id,
            name=self.name if self.name is not None else existing_team.name,
            salt_argon=self.salt_argon if self.salt_argon is not None else existing_team.salt_argon
        )
        
class DeleteTeamDTO(BaseModel):
    id: UUID