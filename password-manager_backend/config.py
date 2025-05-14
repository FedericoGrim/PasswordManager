from dependency_injector import containers, providers
from Infrastructure.Repositories.postgreSQL import UserService
from Application.UseCase.UserUseCase import CreateUserUseCase, GetUserByEmailUseCase, UpdateUserUseCase, DeleteUserUseCase

class Container(containers.DeclarativeContainer):

    WiringConfig = containers.WiringConfiguration(modules=["Presentation.Routes.UserRouter"])

    UserRepositoryFactory = providers.Factory(UserService)

    CreateUserUseCaseProvider = providers.Factory(
        CreateUserUseCase,
        UserRepository=UserRepositoryFactory
    )

    GetUserUseCaseProvider = providers.Factory(
        GetUserByEmailUseCase,
        UserRepository=UserRepositoryFactory
    )

    UpdateUserUseCaseProvider = providers.Factory(
        UpdateUserUseCase,
        UserRepository=UserRepositoryFactory
    )

    DeleteUserUseCaseProvider = providers.Factory(
        DeleteUserUseCase,
        UserRepository=UserRepositoryFactory
    )