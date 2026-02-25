from pydantic import BaseModel
from typing import Optional
from uuid import UUID

from domain.entities.team_members import TeamMembers
        
class TeamMembersDTO(BaseModel):
    id: UUID
    user_id: UUID
    team_id: UUID
    role: str

    def to_entity(self):
        return TeamMembers(
            user_id=self.user_id,
            team_id=self.team_id,
            role=self.role
        )

class CreateTeamMembersDTO(BaseModel):
    user_id: UUID
    team_id: UUID
    role: str

    def to_entity(self):
        return TeamMembers(
            user_id=self.user_id,
            team_id=self.team_id,
            role=self.role
        )

class UpdateTeamMembersDTO(BaseModel):
    role: Optional[str]

    def to_entity(self, existing_member: TeamMembers):
        return TeamMembers(
            user_id=UUID(str(existing_member.user_id)),
            team_id=UUID(str(existing_member.team_id)),
            role=str(self.role)
        )
        
