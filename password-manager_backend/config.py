from dependency_injector import containers, providers

from Infrastructure.Databases.SQL.LocalUserPostgreSQL import LocalUserService as LocalUserService
from Infrastructure.Databases.SQL.SubAccountPostgreSQL import SubAccountService as SubAccountService

from Application.UseCase.LocalUserUseCase import (
    CreateLocalUserUseCase as CreateLocalUserUseCase,
    GetLocalUsersByMainUserIdUseCase as GetLocalUsersByMainUserIdUseCase,
    UpdateLocalUserByIdUseCase as UpdateLocalUserByIdUseCase,
    DeleteLocalUserByIdUseCase as DeleteLocalUserByIdUseCase
)

from Application.UseCase.SubAccountUseCases import (
    CreateSubAccountUseCase as CreateSubAccountUseCase,
    GetAllSubAccountsByLocalUserIdUseCase as GetAllSubAccountsByLocalUserIdUseCase,
    UpdateSubAccountByIdUseCase as UpdateSubAccountByIdUseCase,
    DeleteSubAccountByIdUseCase as DeleteSubAccountByIdUseCase
)

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

class SQLContainer(containers.DeclarativeContainer):
    local_user = providers.Container(LocalUserContainer)
    subaccount = providers.Container(SubAccountContainer)

class Container(containers.DeclarativeContainer):
    SQL = providers.Container(SQLContainer)