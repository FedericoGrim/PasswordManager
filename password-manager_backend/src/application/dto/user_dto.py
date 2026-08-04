from pydantic import BaseModel
from typing import Optional
from uuid import UUID

from domain.entities.user import User

class UserDTO(BaseModel):
    id: UUID
    id_keycloak: UUID

    username: str
    code: str

    public_key: bytes
    private_key: bytes

    @classmethod
    def from_entity(cls, entity: User) -> "UserDTO":
        return cls(
            id=entity.id,
            id_keycloak=entity.id_keycloak,
            username=entity.username,
            code=entity.code,
            public_key=entity.public_key,
            private_key=entity.private_key,
        )

    def to_entity(self) -> User:
        return User(
            id_keycloak=self.id_keycloak,
            username=self.username,
            code=self.code,
            public_key=self.public_key,
            private_key=self.private_key,
        )
class CreateUserDTO(BaseModel):
    id_keycloak: UUID
    username: str

    def to_entity(self):
        return User(
            id_keycloak=self.id_keycloak,
            username=self.username,
        )

class UpdateUserDTO(BaseModel):
    id_keycloak: Optional[UUID]
    username: Optional[str]

    def to_entity(self, existing_user: User):
        return User(
            id=existing_user.id,
            id_keycloak=self.id_keycloak if self.id_keycloak is not None else existing_user.id_keycloak,
            username=self.username if self.username is not None else existing_user.username,
        )