from dependency_injector import containers, providers

from Infrastructure.Databases.SQL.UserPostgreSQL import UserService
from Infrastructure.Databases.SQL.SubAccountPostgreSQL import SubAccountService

from Application.UseCase.UserUseCase import (
    CreateUserUseCase,
    GetUsersByMainUserIdUseCase,
    UpdateUserByIdUseCase,
    DeleteUserByIdUseCase,
)

from Application.UseCase.SubAccountUseCases import (
    CreateSubAccountUseCase,
    GetAllSubAccountsByLocalUserIdUseCase,
    UpdateSubAccountByIdUseCase,
    DeleteSubAccountByIdUseCase,
)

from Infrastructure.Databases.NoSQL.EventsMongoDB import EventRepository


# ------------------- SQL Containers -------------------
class UserContainer(containers.DeclarativeContainer):
    UserRepositoryFactory = providers.Factory(UserService, db=providers.Dependency())

    CreateUserProvider = providers.Factory(
        CreateUserUseCase,
        UserRepository=UserRepositoryFactory,
    )
    GetUserByKeycloakIdProvider = providers.Factory(
        GetUsersByMainUserIdUseCase,
        UserRepository=UserRepositoryFactory,
    )
    UpdateUserByIdProvider = providers.Factory(
        UpdateUserByIdUseCase,
        UserRepository=UserRepositoryFactory,
    )
    DeleteUserByIdProvider = providers.Factory(
        DeleteUserByIdUseCase,
        UserRepository=UserRepositoryFactory,
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
    user = providers.Container(UserContainer)
    subaccount = providers.Container(SubAccountContainer)


class NoSQLContainer(containers.DeclarativeContainer):
    events = providers.Container(EventsContainer)


class Container(containers.DeclarativeContainer):
    SQL = providers.Container(SQLContainer)
    NoSQL = providers.Container(NoSQLContainer)
