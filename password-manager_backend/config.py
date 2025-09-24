from dependency_injector import containers, providers

from Infrastructure.Repositories.V1.LocalUserPostgreSQL import LocalUserService as LocalUserServiceV1
from Infrastructure.Repositories.V1.SubAccountPostgreSQL import SubAccountService as SubAccountServiceV1

from Application.UseCase.V1.LocalUserUseCase import (
    CreateLocalUserUseCase as CreateLocalUserUseCaseV1,
    GetLocalUsersByMainUserIdUseCase as GetLocalUsersByMainUserIdUseCaseV1,
    UpdateLocalUserByIdUseCase as UpdateLocalUserByIdUseCaseV1,
    DeleteLocalUserByIdUseCase as DeleteLocalUserByIdUseCaseV1
)

from Application.UseCase.V1.SubAccountUseCases import (
    CreateSubAccountUseCase as CreateSubAccountUseCaseV1,
    GetAllSubAccountsByLocalUserIdUseCase as GetAllSubAccountsByLocalUserIdUseCaseV1,
    UpdateSubAccountByIdUseCase as UpdateSubAccountByIdUseCaseV1,
    DeleteSubAccountByIdUseCase as DeleteSubAccountByIdUseCaseV1
)

from Infrastructure.Repositories.V2.LocalUserPostgreSQL import LocalUserService as LocalUserServiceV2
from Infrastructure.Repositories.V2.SubAccountPostgreSQL import SubAccountService as SubAccountServiceV2

from Application.UseCase.V2.LocalUserUseCase import (
    CreateLocalUserUseCase as CreateLocalUserUseCaseV2,
    GetLocalUsersByMainUserIdUseCase as GetLocalUsersByMainUserIdUseCaseV2,
    UpdateLocalUserByIdUseCase as UpdateLocalUserByIdUseCaseV2,
    DeleteLocalUserByIdUseCase as DeleteLocalUserByIdUseCaseV2
)

from Application.UseCase.V2.SubAccountUseCases import (
    CreateSubAccountUseCase as CreateSubAccountUseCaseV2,
    GetAllSubAccountsByLocalUserIdUseCase as GetAllSubAccountsByLocalUserIdUseCaseV2,
    UpdateSubAccountByIdUseCase as UpdateSubAccountByIdUseCaseV2,
    DeleteSubAccountByIdUseCase as DeleteSubAccountByIdUseCaseV2
)

class LocalUserContainerV1(containers.DeclarativeContainer):
    LocalUserRepositoryFactory = providers.Factory(LocalUserServiceV1, db=providers.Dependency())

    CreateLocalUserProvider = providers.Factory(
        CreateLocalUserUseCaseV1,
        LocalUserRepository=LocalUserRepositoryFactory,
    )
    GetLocalUserByKeycloakIdProvider = providers.Factory(
        GetLocalUsersByMainUserIdUseCaseV1,
        LocalUserRepository=LocalUserRepositoryFactory,
    )
    UpdateLocalUserByIdProvider = providers.Factory(
        UpdateLocalUserByIdUseCaseV1,
        LocalUserRepository=LocalUserRepositoryFactory,
    )
    DeleteLocalUserByIdProvider = providers.Factory(
        DeleteLocalUserByIdUseCaseV1,
        LocalUserRepository=LocalUserRepositoryFactory,
    )

class SubAccountContainerV1(containers.DeclarativeContainer):
    SubAccountRepositoryFactory = providers.Factory(SubAccountServiceV1, db=providers.Dependency())
    
    CreateSubAccountProvider = providers.Factory(
        CreateSubAccountUseCaseV1,
        SubAccountRepository=SubAccountRepositoryFactory,
    )
    GetAllSubAccountsByUserIdProvider = providers.Factory(
        GetAllSubAccountsByLocalUserIdUseCaseV1,
        SubAccountRepository=SubAccountRepositoryFactory,
    )
    UpdateSubAccountByIdProvider = providers.Factory(
        UpdateSubAccountByIdUseCaseV1,
        SubAccountRepository=SubAccountRepositoryFactory,
    )
    DeleteSubAccountByIdProvider = providers.Factory(
        DeleteSubAccountByIdUseCaseV1,
        SubAccountRepository=SubAccountRepositoryFactory,
    )

class LocalUserContainerV2(containers.DeclarativeContainer):
    LocalUserRepositoryFactory = providers.Factory(LocalUserServiceV2, db=providers.Dependency())

    CreateLocalUserProvider = providers.Factory(
        CreateLocalUserUseCaseV2,
        LocalUserRepository=LocalUserRepositoryFactory,
    )
    GetLocalUserByKeycloakIdProvider = providers.Factory(
        GetLocalUsersByMainUserIdUseCaseV2,
        LocalUserRepository=LocalUserRepositoryFactory,
    )
    UpdateLocalUserByIdProvider = providers.Factory(
        UpdateLocalUserByIdUseCaseV2,
        LocalUserRepository=LocalUserRepositoryFactory,
    )
    DeleteLocalUserByIdProvider = providers.Factory(
        DeleteLocalUserByIdUseCaseV2,
        LocalUserRepository=LocalUserRepositoryFactory,
    )

class SubAccountContainerV2(containers.DeclarativeContainer):
    SubAccountRepositoryFactory = providers.Factory(SubAccountServiceV2, db=providers.Dependency())

    CreateSubAccountProvider = providers.Factory(
        CreateSubAccountUseCaseV2,
        SubAccountRepository=SubAccountRepositoryFactory,
    )
    GetAllSubAccountsByUserIdProvider = providers.Factory(
        GetAllSubAccountsByLocalUserIdUseCaseV2,
        SubAccountRepository=SubAccountRepositoryFactory,
    )
    UpdateSubAccountByIdProvider = providers.Factory(
        UpdateSubAccountByIdUseCaseV2,
        SubAccountRepository=SubAccountRepositoryFactory,
    )
    DeleteSubAccountByIdProvider = providers.Factory(
        DeleteSubAccountByIdUseCaseV2,
        SubAccountRepository=SubAccountRepositoryFactory,
    )

class ContainerV1(containers.DeclarativeContainer):
    local_user = providers.Container(LocalUserContainerV1)
    subaccount = providers.Container(SubAccountContainerV1)

class ContainerV2(containers.DeclarativeContainer):
    local_user = providers.Container(LocalUserContainerV2)
    subaccount = providers.Container(SubAccountContainerV2)

class Container(containers.DeclarativeContainer):
    V1 = providers.Container(ContainerV1)
    V2 = providers.Container(ContainerV2)