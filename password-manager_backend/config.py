from dependency_injector import containers, providers

from Infrastructure.Databases.SQL.UserPostgreSQL import UserService
from Infrastructure.Databases.SQL.SubAccountPostgreSQL import SubAccountService

from Infrastructure.Databases.SQL.TeamPostgreSQL import TeamService

from Application.UseCase.UserUseCase import (
    CreateUserUseCase,
    GetUsersByMainUserIdUseCase,
    UpdateUserByIdUseCase,
    DeleteUserByIdUseCase,
)

from Application.UseCase.SubAccountUseCase import (
    CreateSubAccountUseCase,
    GetAllSubAccountsByLocalUserIdUseCase,
    UpdateSubAccountByIdUseCase,
    DeleteSubAccountByIdUseCase,
)

from Application.UseCase.TeamUseCase import (
    CreateTeamUseCase,
    GetTeamsByUserIdUseCase,
    GetTeamsByUserIdUseCase,
    UpdateTeamByIdUseCase,
    DeleteTeamByIdUseCase,
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


class TeamContainer(containers.DeclarativeContainer):
    TeamRepositoryFactory = providers.Factory(TeamService, db=providers.Dependency())

    CreateTeamProvider = providers.Factory(
        CreateTeamUseCase,
        TeamRepository=TeamRepositoryFactory,
    )
    GetTeamByIdProvider = providers.Factory(
        GetTeamsByUserIdUseCase,
        TeamRepository=TeamRepositoryFactory,
    )
    GetTeamsByUserIdProvider = providers.Factory(
        GetTeamsByUserIdUseCase,
        TeamRepository=TeamRepositoryFactory,
    )
    UpdateTeamByIdProvider = providers.Factory(
        UpdateTeamByIdUseCase,
        TeamRepository=TeamRepositoryFactory,
    )
    DeleteTeamByIdProvider = providers.Factory(
        DeleteTeamByIdUseCase,
        TeamRepository=TeamRepositoryFactory,
    )


# ------------------- NoSQL Container -------------------
class EventsContainer(containers.DeclarativeContainer):
    mongo_client = providers.Dependency()
    EventRepositoryProvider = providers.Factory(EventRepository, mongo_client=mongo_client)


# ------------------- Aggregated Containers -------------------
class SQLContainer(containers.DeclarativeContainer):
    user = providers.Container(UserContainer)
    subaccount = providers.Container(SubAccountContainer)
    team = providers.Container(TeamContainer)


class NoSQLContainer(containers.DeclarativeContainer):
    events = providers.Container(EventsContainer)


class Container(containers.DeclarativeContainer):
    SQL = providers.Container(SQLContainer)
    NoSQL = providers.Container(NoSQLContainer)
