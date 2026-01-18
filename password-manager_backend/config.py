from dependency_injector import containers, providers

from Infrastructure.Databases.SQL.UserPostgreSQL import UserService
from Infrastructure.Databases.SQL.SubAccountPostgreSQL import SubAccountService
from Infrastructure.Databases.SQL.TeamPostgreSQL import TeamService
from Infrastructure.Databases.SQL.TeamMembersPostgreSQL import TeamMembersService
from Infrastructure.Databases.SQL.CategoriesPostgreSQL import CategoriesService
from Infrastructure.Databases.SQL.SubAccauntCategoriesPostgreSQL import SubAccauntCategoriesService

from Application.UseCase.UserUseCase import (
    CreateUserUseCase,
    GetUsersByKeycloakIdUseCase,
    UpdateUserByIdUseCase,
    DeleteUserByIdUseCase,
)

from Application.UseCase.SubAccountUseCase import (
    CreateSubAccountUseCase,
    GetAllSubAccountsByTeamIdUseCase,
    UpdateSubAccountByIdUseCase,
    DeleteSubAccountByIdUseCase,
)

from Application.UseCase.TeamUseCase import (
    CreateTeamUseCase,
    GetTeamByIdUseCase,
    GetTeamsByUserIdUseCase,
    GetTeamsByUserIdUseCase,
    UpdateTeamByIdUseCase,
    DeleteTeamByIdUseCase,
)

from Application.UseCase.TeamMembersUseCase import (
    AddMemberToTeamUseCase,
    GetTeamMembersByTeamIdUseCase,
    GetTeamsByMemberIdUseCase,
    UpdateTeamMemberRoleUseCase,
    RemoveMemberFromTeamUseCase
)

from Application.UseCase.CategoriesUseCase import (
    CreateCategoriesUseCase,
    GetAllCategoriesByTeamIdUseCase,
    UpdateCategoryByIdUseCase,
    DeleteCategoryByIdUseCase,
)

from Application.UseCase.SubAccountCategoriesUseCase import (
    CreateSubAccountCategoryUseCase,
    GetAllCategoriesBySubAccountIdUseCase,
    UpdateSubAccountCategoryUseCase,
    DeleteSubAccountCategoryUseCase,
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
        GetUsersByKeycloakIdUseCase,
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
    GetAllSubAccountsByTeamIdProvider = providers.Factory(
        GetAllSubAccountsByTeamIdUseCase,
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
        GetTeamByIdUseCase,
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

class TeamMembersContainer(containers.DeclarativeContainer):
    TeamMembersRepositoryFactory = providers.Factory(TeamMembersService, db=providers.Dependency())

    AddMemberToTeamProvider = providers.Factory(
        AddMemberToTeamUseCase,
        TeamMembersRepository=TeamMembersRepositoryFactory,
    )
    GetTeamMembersByTeamIdProvider = providers.Factory(
        GetTeamMembersByTeamIdUseCase,
        TeamMembersRepository=TeamMembersRepositoryFactory,
    )
    GetTeamsByMemberIdProvider = providers.Factory(
        GetTeamsByMemberIdUseCase,
        TeamMembersRepository=TeamMembersRepositoryFactory,
    )
    UpdateTeamMemberRoleProvider = providers.Factory(
        UpdateTeamMemberRoleUseCase,
        TeamMembersRepository=TeamMembersRepositoryFactory,
    )
    RemoveMemberFromTeamProvider = providers.Factory(
        RemoveMemberFromTeamUseCase,
        TeamMembersRepository=TeamMembersRepositoryFactory,
    )

class CategoriesContainer(containers.DeclarativeContainer):
    CategoriesRepositoryFactory = providers.Factory(CategoriesService, db=providers.Dependency())

    CreateCategoriesProvider = providers.Factory(
        CreateCategoriesUseCase,
        CategoriesRepository=CategoriesRepositoryFactory,
    )
    GetAllCategoriesByTeamIdProvider = providers.Factory(
        GetAllCategoriesByTeamIdUseCase,
        CategoriesRepository=CategoriesRepositoryFactory,
    )
    UpdateCategoryByIdProvider = providers.Factory(
        UpdateCategoryByIdUseCase,
        CategoriesRepository=CategoriesRepositoryFactory,
    )
    DeleteCategoryByIdProvider = providers.Factory(
        DeleteCategoryByIdUseCase,
        CategoriesRepository=CategoriesRepositoryFactory,
    )

class SubAccountCategoriesContainer(containers.DeclarativeContainer):
    SubAccountCategoriesRepositoryFactory = providers.Factory(SubAccauntCategoriesService, db=providers.Dependency())

    CreateSubAccountCategoryProvider = providers.Factory(
        CreateSubAccountCategoryUseCase,
        SubAccountCategoriesRepository=SubAccountCategoriesRepositoryFactory,
    )
    GetAllCategoriesBySubAccountIdProvider = providers.Factory(
        GetAllCategoriesBySubAccountIdUseCase,
        SubAccountCategoriesRepository=SubAccountCategoriesRepositoryFactory,
    )
    UpdateSubAccountCategoryProvider = providers.Factory(
        UpdateSubAccountCategoryUseCase,
        SubAccountCategoriesRepository=SubAccountCategoriesRepositoryFactory,
    )
    DeleteSubAccountCategoryProvider = providers.Factory(
        DeleteSubAccountCategoryUseCase,
        SubAccountCategoriesRepository=SubAccountCategoriesRepositoryFactory,
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
    team_members = providers.Container(TeamMembersContainer)
    categories = providers.Container(CategoriesContainer)
    sub_account_categories = providers.Container(SubAccountCategoriesContainer)


class NoSQLContainer(containers.DeclarativeContainer):
    events = providers.Container(EventsContainer)


class Container(containers.DeclarativeContainer):
    SQL = providers.Container(SQLContainer)
    NoSQL = providers.Container(NoSQLContainer)
