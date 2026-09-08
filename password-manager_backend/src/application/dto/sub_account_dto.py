from pydantic import BaseModel, UUID4
from typing import Optional

from domain.entities.sub_account import SubAccount

class SubAccountDTO(BaseModel):
    id: UUID4
    team_id: UUID4
    username_encrypted: str
    email_encrypted: str
    password_encrypted: str
    site_link_encrypted: str
    required_perm_level_id: UUID4

    def to_entity(self):
        return SubAccount(
            team_id=self.team_id,
            username_encrypted=self.username_encrypted,
            email_encrypted=self.email_encrypted,
            password_encrypted=self.password_encrypted,
            site_link_encrypted=self.site_link_encrypted,
            required_perm_level_id=self.required_perm_level_id
        )

class CreateSubAccountDTO(BaseModel):
    team_id: UUID4
    username_encrypted: str
    email_encrypted: str
    password_encrypted: str
    site_link_encrypted: str
    required_perm_level_id: UUID4

    def to_entity(self):
        return SubAccount(
            team_id=self.team_id,
            username_encrypted=self.username_encrypted,
            email_encrypted=self.email_encrypted,
            password_encrypted=self.password_encrypted,
            site_link_encrypted=self.site_link_encrypted,
            required_perm_level_id=self.required_perm_level_id
        )

class UpdateSubAccountDTO(BaseModel):
    id: UUID4
    username_encrypted: Optional[str]
    email_encrypted: Optional[str]
    password_encrypted: Optional[str]
    site_link_encrypted: Optional[str]
    required_perm_level_id: Optional[UUID4]

    def to_entity(self, existing_sub_account: SubAccount):
        return SubAccount(
            team_id=existing_sub_account.team_id,
            username_encrypted=self.username_encrypted if self.username_encrypted is not None else existing_sub_account.username_encrypted,
            email_encrypted=self.email_encrypted if self.email_encrypted is not None else existing_sub_account.email_encrypted,
            password_encrypted=self.password_encrypted if self.password_encrypted is not None else existing_sub_account.password_encrypted,
            site_link_encrypted=self.site_link_encrypted if self.site_link_encrypted is not None else existing_sub_account.site_link_encrypted,
            required_perm_level_id=self.required_perm_level_id if self.required_perm_level_id is not None else existing_sub_account.required_perm_level_id
        )
        
class DeleteSubAccountDTO(BaseModel):
    id: UUID4