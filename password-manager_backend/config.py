from dependency_injector import containers, providers

from Infrastructure.Repositories.LocalUserPostgreSQL import LocalUserService

from Application.UseCase.LocalUserUseCase import CreateLocalUserUseCase, GetAllLocalUsersByMainUserIdUseCase, UpdateLocalUserByIdUseCase, DeleteLocalUserByIdUseCase
#from Application.UseCase.SubaccountUseCase import CreateSubaccountUseCase, GetAllSubaccountsByUserIdUseCase, UpdateSubaccountByIdUseCase, DeleteSubaccountByIdUseCase

class Container(containers.DeclarativeContainer):
    LocalUserRepositoryFactory = providers.Factory(LocalUserService)

    CreateLocalUserProvider = providers.Factory(
        CreateLocalUserUseCase,
        LocalUserRepository=LocalUserRepositoryFactory,
    )
    GetAllLocalUsersByMainUserIdProvider = providers.Factory(
        GetAllLocalUsersByMainUserIdUseCase,
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
