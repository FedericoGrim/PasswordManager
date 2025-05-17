from dependency_injector import containers, providers
from Infrastructure.Repositories.UserPostgreSQL import UserService
from Application.UseCase.UserUseCase import CreateUserUseCase, GetUserByEmailUseCase, UpdateUserUsernameUseCase, UpdateUserEmailUseCase, UpdateUserPasswordUseCase, DeleteUserUseCase

class Container(containers.DeclarativeContainer):
    UserRepositoryFactory = providers.Factory(UserService)

    CreateUserUseCaseProvider = providers.Factory(
        CreateUserUseCase,
        UserRepository=UserRepositoryFactory
    )

    GetUserUseCaseProvider = providers.Factory(
        GetUserByEmailUseCase,
        UserRepository=UserRepositoryFactory
    )

    UpdateUserUsernameUseCaseProvider = providers.Factory(
        UpdateUserUsernameUseCase,
        UserRepository=UserRepositoryFactory
    )

    UpdateUserEmailUseCaseProvider = providers.Factory(
        UpdateUserEmailUseCase,
        UserRepository=UserRepositoryFactory
    )

    UpdateUserPasswrordUseCaseProvider = providers.Factory(
        UpdateUserPasswordUseCase,
        UserRepository=UserRepositoryFactory
    )

    DeleteUserUseCaseProvider = providers.Factory(
        DeleteUserUseCase,
        UserRepository=UserRepositoryFactory
    )