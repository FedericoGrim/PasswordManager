from dependency_injector import containers, providers

from Infrastructure.Databases.SQL.LocalUserPostgreSQL import LocalUserService
from Infrastructure.Databases.SQL.SubAccountPostgreSQL import SubAccountService

from Application.UseCase.LocalUserUseCase import (
    CreateLocalUserUseCase,
    GetLocalUsersByMainUserIdUseCase,
    UpdateLocalUserByIdUseCase,
    DeleteLocalUserByIdUseCase,
)

from Application.UseCase.SubAccountUseCases import (
    CreateSubAccountUseCase,
    GetAllSubAccountsByLocalUserIdUseCase,
    UpdateSubAccountByIdUseCase,
    DeleteSubAccountByIdUseCase,
)

from Infrastructure.Databases.NoSQL.EventsMongoDB import EventRepository


# ------------------- SQL Containers -------------------
class LocalUserContainer(containers.DeclarativeContainer):
    LocalUserRepositoryFactory = providers.Factory(LocalUserService, db=providers.Dependency())

    CreateLocalUserProvider = providers.Factory(
        CreateLocalUserUseCase,
        LocalUserRepository=LocalUserRepositoryFactory,
    )
    GetLocalUserByKeycloakIdProvider = providers.Factory(
        GetLocalUsersByMainUserIdUseCase,
        LocalUserRepository=LocalUserRepositoryFactory,
    )
    UpdateLocalUserByIdProvider = providers.Factory(
        UpdateLocalUserByIdUseCase,
        LocalUserRepository=LocalUserRepositoryFactory,
    )
    DeleteLocalUserByIdProvider = providers.Factory(
        DeleteLocalUserByIdUseCase,
        LocalUserRepository=LocalUserRepositoryFactory,
    )


class SubAccountContainer(containers.DeclarativeContainer):
    SubAccountRepositoryFactory = providers.Factory(SubAccountService, db=providers.Dependency())

    CreateSubAccountProvider = providers.Factory(
        CreateSubAccountUseCase,
        SubAccountRepository=SubAccountRepositoryFactory,
    )
    GetAllSubAccountsByUserIdProvider = providers.Factory(
        GetAllSubAccountsByLocalUserIdUseCase,
        SubAccountRepository=SubAccountRepositoryFactory,
    )
    UpdateSubAccountByIdProvider = providers.Factory(
        UpdateSubAccountByIdUseCase,
        SubAccountRepository=SubAccountRepositoryFactory,
    )
    DeleteSubAccountByIdProvider = providers.Factory(
        DeleteSubAccountByIdUseCase,
        SubAccountRepository=SubAccountRepositoryFactory,
    )


# ------------------- NoSQL Container -------------------
class EventsContainer(containers.DeclarativeContainer):
    mongo_client = providers.Dependency()
    EventRepositoryProvider = providers.Factory(EventRepository, mongo_client=mongo_client)


# ------------------- Aggregated Containers -------------------
class SQLContainer(containers.DeclarativeContainer):
    local_user = providers.Container(LocalUserContainer)
    subaccount = providers.Container(SubAccountContainer)


class NoSQLContainer(containers.DeclarativeContainer):
    events = providers.Container(EventsContainer)


class Container(containers.DeclarativeContainer):
    SQL = providers.Container(SQLContainer)
    NoSQL = providers.Container(NoSQLContainer)
