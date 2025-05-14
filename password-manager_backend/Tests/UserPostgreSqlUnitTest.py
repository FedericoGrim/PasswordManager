import unittest
from unittest.mock import MagicMock
from Application.UseCase.UserUseCase import CreateUserUseCase
from Domain.Objects.UserObj import UserCreate
from Application.Exceptions.UserUseCaseExceptions import UserCreationException

class TestCreateUserUseCase(unittest.TestCase):
    def setUp(self):
        self.user_repository_mock = MagicMock()
        self.user_create = UserCreate(
            username="John Doe",
            email="john.doe@example.com",
            password="securepassword"
        )
        self.create_user_use_case = CreateUserUseCase(self.user_repository_mock)

    def test_create_user_success(self):
        self.user_repository_mock.CreateUser.return_value = {
            "id": 1,
            "username": "John Doe",
            "email": "john.doe@example.com",
            "password": "securepassword"
        }

        result = self.create_user_use_case.execute(self.user_create)

        self.assertEqual(result["username"], "John Doe")
        self.assertEqual(result["email"], "john.doe@example.com")
        self.assertEqual(result["password"], "securepassword")

    def test_create_user_failure(self):
        self.user_repository_mock.CreateUser.side_effect = Exception("Database error")

        with self.assertRaises(UserCreationException):
            self.create_user_use_case.execute(self.user_create)

if __name__ == '__main__':
    unittest.main()
