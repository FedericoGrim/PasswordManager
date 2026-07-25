from pydantic import BaseModel
from typing import Optional
from uuid import UUID

from domain.entities.user_teams_keys import UserTeamsKeys

class UserTeamsKeyDTO(BaseModel):
    id: UUID
    user_id: UUID
    team_id: UUID
    key: str

    def to_entity(self):
        return UserTeamsKeys(
            user_id=self.user_id,
            team_id=self.team_id,
            key=self.key
        )

class CreateUserTeamsKeyDTO(BaseModel):
    user_id: UUID
    team_id: UUID
    key: str

    def to_entity(self):
        return UserTeamsKeys(
            user_id=self.user_id,
            team_id=self.team_id,
            key=self.key
        )

class UpdateUserTeamsKeyDTO(BaseModel):
    user_id: UUID
    team_id: UUID
    key: Optional[str]

    def to_entity(self, existing_key: UserTeamsKeys):
        return UserTeamsKeys(
            user_id=UUID(str(existing_key.user_id)),
            team_id=UUID(str(existing_key.team_id)),
            key=str(self.key)
        )

class RemoveUserTeamsKeyDTO(BaseModel):
    user_id: UUID
    team_id: UUID
