from dependency_injector import containers, providers

from Infrastructure.Repositories.LocalUserPostgreSQL import LocalUserService

from Application.UseCase.LocalUserUseCase import CreateLocalUserUseCase, GetAllLocalUsersByMainUserIdUseCase, UpdateLocalUserByIdUseCase, DeleteLocalUserByIdUseCase
#from Application.UseCase.SubaccountUseCase import CreateSubaccountUseCase, GetAllSubaccountsByUserIdUseCase, UpdateSubaccountByIdUseCase, DeleteSubaccountByIdUseCase

class LocalUserCRUD(containers.DeclarativeContainer):
    LocalUserRepositoryFactory = providers.Factory(LocalUserService)
        
    CreateLocalUserProvider = providers.Factory(
        CreateLocalUserUseCase,
        UserRepository=LocalUserRepositoryFactory
    )

    GetAllLocalUserByIdProvider = providers.Factory(
        GetAllLocalUsersByMainUserIdUseCase,
        UserRepository=LocalUserRepositoryFactory
    )

    UpdateLocalUserByIdProvider = providers.Factory(
        UpdateLocalUserByIdUseCase,
        UserRepository=LocalUserRepositoryFactory
    )

    DeleteUserByIdUseCaseProvider = providers.Factory(
    DeleteLocalUserByIdUseCase,
    UserRepository=LocalUserRepositoryFactory
)

#class SubaccountCRUD:
    
    
class Container(containers.DeclarativeContainer):
    LocalUserCRUD = providers.Container(LocalUserCRUD)