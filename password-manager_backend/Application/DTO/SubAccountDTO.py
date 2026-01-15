from pydantic import BaseModel, UUID4, StringConstraints
from typing import Optional, Annotated

from Domain.Entities.SubAccount import SubAccount

class SubAccountDTO(BaseModel):
    id: UUID4
    team_id: UUID4
    title: str
    username: str
    email: str
    password: str
    url: str
    necessary_role: str

    def to_entity(self):
        return SubAccount(
            team_id=self.team_id,
            title=self.title,
            username=self.username,
            email=self.email,
            password=self.password,
            link=self.url,
            necessary_role=self.necessary_role
        )

class CreateSubAccountDTO(BaseModel):
    team_id: UUID4
    title: Annotated[str, StringConstraints(min_length=1)]
    username: str
    email: str
    password: str
    url: str
    necessary_role: Annotated[str, StringConstraints(min_length=1)]

    def to_entity(self):
        return SubAccount(
            team_id=self.team_id,
            title=self.title,
            username=self.username,
            email=self.email,
            password=self.password,
            link=self.url,
            necessary_role=self.necessary_role
        )

class UpdateSubAccountDTO(BaseModel):
    title: Optional[Annotated[str, StringConstraints(min_length=1)]]
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]
    url: Optional[str]
    necessary_role: Optional[Annotated[str, StringConstraints(min_length=1)]]

    def to_entity(self, existing_sub_account: SubAccount):
        return SubAccount(
            team_id=existing_sub_account.team_id,
            title=self.title if self.title is not None else existing_sub_account.title,
            username=self.username if self.username is not None else existing_sub_account.username,
            email=self.email if self.email is not None else existing_sub_account.email,
            password=self.password if self.password is not None else existing_sub_account.password,
            link=self.url if self.url is not None else existing_sub_account.link,
            necessary_role=self.necessary_role if self.necessary_role is not None else existing_sub_account.necessary_role
        )