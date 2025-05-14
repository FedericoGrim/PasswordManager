import unittest
from unittest.mock import MagicMock
from Application.UseCase.UserUseCase import CreateUserUseCase
from Domain.Objects.UserObj import UserCreate, UserUpdate
from Application.Exceptions.UserUseCaseExceptions import UserCreationException, UserRetrievalException, UserUpdateException, UserDeletionException

class TestCreateUserUseCase(unittest.TestCase):
    def setUp(self):
        self.user_repository_mock = MagicMock()
        self.user_create = UserCreate(
            username="John Doe",
            email="john.doe@example.com",
            password="securepassword"
        )
        self.user_update = UserUpdate(
            username="John Doe Updated",
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
        self.user_repository_mock.CreateUser.side_effect = UserCreationException("User already exists")

        with self.assertRaises(UserCreationException):
            self.create_user_use_case.execute(self.user_create)

    def test_get_user_success(self):
        self.user_repository_mock.GetUser.return_value = {
            "id": 1,
            "username": "John Doe",
            "email": "john.doe@example.com",
            "password": "securepassword"
        }

        result = self.user_repository_mock.GetUser("john.doe@example.com")

        self.assertEqual(result["username"], "John Doe")
        self.assertEqual(result["email"], "john.doe@example.com")
        self.assertEqual(result["password"], "securepassword")

    def test_get_user_not_found(self):
        self.user_repository_mock.GetUser.side_effect = UserRetrievalException("User not found")

        with self.assertRaises(UserRetrievalException):
            self.user_repository_mock.GetUser("notfound@example.com")

    def test_update_user_success(self):
        self.user_repository_mock.UpdateUser.return_value = {
            "id": 1,
            "username": "John Doe Updated",
            "email": "john.doe@example.com",
            "password": "securepassword"
        }

        result = self.user_repository_mock.UpdateUser(1, self.user_update)

        self.assertEqual(result["username"], "John Doe Updated")
        self.assertEqual(result["email"], "john.doe@example.com")

    def test_update_user_failure(self):
        self.user_repository_mock.UpdateUser.side_effect = UserUpdateException("Update failed")

        with self.assertRaises(UserUpdateException):
            self.user_repository_mock.UpdateUser(1, self.user_update)

    def test_delete_user_success(self):
        self.user_repository_mock.DeleteUser.return_value = {
            "id": 1,
            "username": "John Doe",
            "email": "john.doe@example.com"
        }

        result = self.user_repository_mock.DeleteUser(1)
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["username"], "John Doe")

    def test_delete_user_failure(self):
        self.user_repository_mock.DeleteUser.side_effect = UserDeletionException("Delete failed")

        with self.assertRaises(UserDeletionException):
            self.user_repository_mock.DeleteUser(1)

if __name__ == '__main__':
    unittest.main()
