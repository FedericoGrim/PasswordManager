import uuid
from Application.DTO.LocalUserDTO import CreateLocalUserDTO
from Application.Exceptions.LocalUserUseCaseExceptions import *

from Application.UseCase.Publisher import EventPublisher

class CreateLocalUserUseCase:
    def __init__(self, LocalUserRepository, EventRepository=None):
        self.LocalUserRepository = LocalUserRepository
        self.EventRepository = EventRepository  # opzionale

    async def execute(self, localuser_create: CreateLocalUserDTO):
        try:
            # Creo l'utente nel DB SQL
            user = self.LocalUserRepository.CreateLocalUser(
                localuser_create, localuser_create.Salt
            )

            # Salvo evento nel NoSQL se presente
            if self.EventRepository:
                EventPublisher.Publish(
                    EventType="UserCreated",
                    Payload={
                        "user_id": str(user.Id),
                        "keycloak_id": str(localuser_create.IdKeycloak)
                    }
                )
            return user
        except Exception as e:
            raise LocalUserCreationException(str(e)) from e


class GetLocalUsersByMainUserIdUseCase:
    def __init__(self, LocalUserRepository):
        self.LocalUserRepository = LocalUserRepository

    def execute(self, mainUserId: uuid.UUID):
        try:
            return self.LocalUserRepository.GetLocalUserById(mainUserId)
        except Exception as e:
            raise LocalUserRetrievalException(str(e)) from e


class UpdateLocalUserByIdUseCase:
    def __init__(self, LocalUserRepository, EventRepository=None):
        self.LocalUserRepository = LocalUserRepository
        self.EventRepository = EventRepository

    async def execute(self, localUserId: uuid.UUID, newSalt: bytes):
        try:
            updated = self.LocalUserRepository.UpdateLocalUserById(localUserId, newSalt)

            if updated and self.EventRepository:
                EventPublisher.Publish(
                    EventType="UserUpdated",
                    Payload={
                        "user_id": str(localUserId),
                        "new_salt": newSalt.decode()
                    }
                )

            return updated
        except Exception as e:
            raise LocalUserUpdateException(str(e)) from e


class DeleteLocalUserByIdUseCase:
    def __init__(self, LocalUserRepository, EventRepository=None):
        self.LocalUserRepository = LocalUserRepository
        self.EventRepository = EventRepository

    async def execute(self, user_id: uuid.UUID):
        try:
            deleted = self.LocalUserRepository.DeleteLocalUserById(user_id)

            if deleted and self.EventRepository:
                EventPublisher.Publish(
                    EventType="UserDeleted",
                    Payload={
                        "user_id": str(user_id)
                    }
                )

            return deleted
        except Exception as e:
            raise LocalUserDeletionException(str(e)) from e
