from pydantic import BaseModel
from typing import Optional
from uuid import UUID

from domain.entities.user import User

class UserDTO(BaseModel):
    id: UUID
    id_keycloak: UUID
    
    public_key: bytes
    private_key: bytes

    @classmethod
    def from_entity(cls, entity: User) -> "UserDTO":
        return cls(
            id=entity.id,
            id_keycloak=entity.id_keycloak,
            public_key=entity.public_key,
            private_key=entity.private_key,
        )

    def to_entity(self) -> User:
        return User(
            id_keycloak=self.id_keycloak,
            public_key=self.public_key,
            private_key=self.private_key,
        )
class CreateUserDTO(BaseModel):
    id_keycloak: UUID

    def to_entity(self):
        return User(
            id_keycloak=self.id_keycloak,
        )
    
class UpdateUserDTO(BaseModel):
    id_keycloak: Optional[UUID]

    def to_entity(self, existing_user: User):
        return User(
            id=existing_user.id,
            id_keycloak=self.id_keycloak if self.id_keycloak is not None else existing_user.id_keycloak
        )