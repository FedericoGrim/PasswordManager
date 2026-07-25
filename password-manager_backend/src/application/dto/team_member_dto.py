from pydantic import BaseModel
from typing import Optional
from uuid import UUID

from domain.entities.team_member import TeamMember
        
class TeamMemberDTO(BaseModel):
    id: UUID
    user_id: UUID
    team_id: UUID
    role: str

    def to_entity(self):
        return TeamMember(
            user_id=self.user_id,
            team_id=self.team_id,
            role=self.role
        )

class CreateTeamMemberDTO(BaseModel):
    user_id: UUID
    team_id: UUID
    role: str

    def to_entity(self):
        return TeamMember(
            user_id=self.user_id,
            team_id=self.team_id,
            role=self.role
        )

class UpdateTeamMemberDTO(BaseModel):
    user_id: UUID
    team_id: UUID
    role: Optional[str]

    def to_entity(self, existing_member: TeamMember):
        return TeamMember(
            user_id=UUID(str(existing_member.user_id)),
            team_id=UUID(str(existing_member.team_id)),
            role=str(self.role)
        )
        
class RemoveTeamMemberDTO(BaseModel):
    member_id: UUID
    team_id: UUID