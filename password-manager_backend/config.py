from dependency_injector import containers, providers

from Infrastructure.Repositories.LocalUserPostgreSQL import LocalUserService
from Infrastructure.Repositories.SubAccountPostgreSQL import SubAccountService

from Application.UseCase.LocalUserUseCase import CreateLocalUserUseCase, GetLocalUsersByMainUserIdUseCase, UpdateLocalUserByIdUseCase, DeleteLocalUserByIdUseCase
from Application.UseCase.SubAccountUseCases import CreateSubAccountUseCase, GetAllSubAccountsByLocalUserIdUseCase, UpdateSubAccountByIdUseCase, DeleteSubAccountByIdUseCase

class LocalUserContainer(containers.DeclarativeContainer):
    LocalUserRepositoryFactory = providers.Factory(LocalUserService, db=providers.Dependency())

    CreateLocalUserProvider = providers.Factory(
        CreateLocalUserUseCase,
        LocalUserRepository=LocalUserRepositoryFactory,
    )
    GetLocalUsersByMainUserIdProvider = providers.Factory(
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

class Container(containers.DeclarativeContainer):
    local_user = providers.Container(LocalUserContainer)
    subaccount = providers.Container(SubAccountContainer)