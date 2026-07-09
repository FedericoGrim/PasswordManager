from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from config import SQLContainer

from dependency_injector import containers, providers

from infrastructure.databases.sql.user_postgreSQL import UserService
from infrastructure.databases.sql.suc_account_postgreSQL import SubAccountService
from infrastructure.databases.sql.team_postgreSQL import TeamService
from infrastructure.databases.sql.team_member_postgreSQL import TeamMembersService
from infrastructure.databases.sql.categories_postgresql import CategoriesService
from infrastructure.databases.sql.sub_account_categories_postgresql import SubAccountCategoriesService



from application.use_case.user_use_case import (
    CreateUserUseCase,
    GetUserByKeycloakIdUseCase,
    UpdateUserByIdUseCase,
    DeleteUserByIdUseCase,
)

from application.use_case.sub_account_use_case import (
    CreateSubAccountUseCase,
    GetSubAccountByIdUseCase,
    GetAllSubAccountsByTeamIdUseCase,
    UpdateSubAccountByIdUseCase,
    DeleteSubAccountByIdUseCase,
)

from application.use_case.team_use_case import (
    CreateTeamUseCase,
    GetTeamByIdUseCase,
    GetTeamsByUserIdUseCase,
    UpdateTeamByIdUseCase,
    DeleteTeamByIdUseCase,
)

from application.use_case.team_member_use_case import (
    AddMemberToTeamUseCase,
    GetTeamMemberByIdUseCase,
    GetTeamMembersByTeamIdUseCase,
    UpdateTeamMemberRoleUseCase,
    RemoveMemberFromTeamUseCase
)

from application.use_case.categories_use_case import (
    CreateCategoriesUseCase,
    GetAllCategoriesByTeamIdUseCase,
    UpdateCategoryByIdUseCase,
    DeleteCategoryByIdUseCase,
)

from application.use_case.sub_account_categories_use_case import (
    CreateSubAccountCategoryUseCase,
    GetAllCategoriesBySubAccountIdUseCase,
    DeleteSubAccountCategoryUseCase,
)


# ------------------- sql Containers -------------------
class UserContainer(containers.DeclarativeContainer):
    UserRepositoryFactory = providers.Factory(UserService, db=providers.Dependency())

    CreateUserProvider = providers.Factory(
        CreateUserUseCase,
        UserRepository=UserRepositoryFactory,
    )
    GetUserByKeycloakIdProvider = providers.Factory(
        GetUserByKeycloakIdUseCase,
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
    GetSubAccountByIdProvider = providers.Factory(
        GetSubAccountByIdUseCase,
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
    
    GetTeamMemberByIdProvider = providers.Factory(
        GetTeamMemberByIdUseCase,
        TeamMembersRepository=TeamMembersRepositoryFactory,
    )
    
    GetTeamMembersByTeamIdProvider = providers.Factory(
        GetTeamMembersByTeamIdUseCase,
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
    SubAccountCategoriesRepositoryFactory = providers.Factory(SubAccountCategoriesService, db=providers.Dependency())

    CreateSubAccountCategoryProvider = providers.Factory(
        CreateSubAccountCategoryUseCase,
        SubAccountCategoriesRepository=SubAccountCategoriesRepositoryFactory,
    )
    GetAllCategoriesBySubAccountIdProvider = providers.Factory(
        GetAllCategoriesBySubAccountIdUseCase,
        SubAccountCategoriesRepository=SubAccountCategoriesRepositoryFactory,
    )

    DeleteSubAccountCategoryProvider = providers.Factory(
        DeleteSubAccountCategoryUseCase,
        SubAccountCategoriesRepository=SubAccountCategoriesRepositoryFactory,
    )

# ------------------- Aggregated Containers -------------------
class SQLContainer(containers.DeclarativeContainer):
    user = providers.Container(UserContainer)
    subaccount = providers.Container(SubAccountContainer)
    team = providers.Container(TeamContainer)
    team_members = providers.Container(TeamMembersContainer)
    categories = providers.Container(CategoriesContainer)
    sub_account_categories = providers.Container(SubAccountCategoriesContainer)


class Container(containers.DeclarativeContainer):
    sql: SQLContainer = providers.Container(SQLContainer)  # type: ignore[assignment]

