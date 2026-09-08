import uuid
from unittest.mock import MagicMock

import pytest

from application.dto.user_teams_keys_dto import CreateUserTeamsKeyDTO, UpdateUserTeamsKeyDTO, RemoveUserTeamsKeyDTO
from application.exceptions.user_teams_keys_use_case_exceptions import (
    UserTeamsKeyAdditionException,
    UserTeamsKeyRetrievalByIdException,
    UserTeamsKeysRetrievalByTeamIdException,
    UserTeamsKeysRetrievalByUserIdException,
    UserTeamsKeyUpdateException,
    UserTeamsKeyRemovalException,
)
from application.use_case.user_teams_keys_use_case import (
    AddUserTeamsKeyUseCase,
    GetUserTeamsKeyByIdUseCase,
    GetUserTeamsKeysByTeamIdUseCase,
    GetUserTeamsKeysByUserIdUseCase,
    UpdateUserTeamsKeyUseCase,
    RemoveUserTeamsKeyUseCase,
)
from domain.entities.user_teams_keys import UserTeamsKeys
from domain.interfaces.user_teams_keys_service_interface import IUserTeamsKeysService


@pytest.fixture
def repo():
    return MagicMock(spec=IUserTeamsKeysService)


def make_key(**overrides):
    defaults = dict(id=uuid.uuid4(), user_id=uuid.uuid4(), team_id=uuid.uuid4(), team_key_encrypted="enc-key")
    defaults.update(overrides)
    return UserTeamsKeys(**defaults)


class TestAddUserTeamsKeyUseCase:
    def test_returns_dto_from_repository_result(self, repo):
        key = make_key()
        repo.add_key.return_value = key

        dto = CreateUserTeamsKeyDTO(user_id=key.user_id, team_id=key.team_id, team_key_encrypted="enc-key")
        result = AddUserTeamsKeyUseCase(repo).execute(uuid.uuid4(), dto)

        assert result.id == key.id

    def test_wraps_repository_errors(self, repo):
        repo.add_key.side_effect = Exception("already exists")
        dto = CreateUserTeamsKeyDTO(user_id=uuid.uuid4(), team_id=uuid.uuid4(), team_key_encrypted="k")

        with pytest.raises(UserTeamsKeyAdditionException):
            AddUserTeamsKeyUseCase(repo).execute(uuid.uuid4(), dto)


class TestGetUserTeamsKeyByIdUseCase:
    def test_returns_dto(self, repo):
        key = make_key()
        repo.get_key_by_id.return_value = key

        result = GetUserTeamsKeyByIdUseCase(repo).execute(key.id)

        assert result.team_key_encrypted == "enc-key"

    def test_wraps_repository_errors(self, repo):
        repo.get_key_by_id.side_effect = Exception("not found")

        with pytest.raises(UserTeamsKeyRetrievalByIdException):
            GetUserTeamsKeyByIdUseCase(repo).execute(uuid.uuid4())


class TestGetUserTeamsKeysByTeamIdUseCase:
    def test_maps_entities_to_dtos(self, repo):
        team_id = uuid.uuid4()
        keys = [make_key(team_id=team_id), make_key(team_id=team_id)]
        repo.get_keys_by_team_id.return_value = keys

        result = GetUserTeamsKeysByTeamIdUseCase(repo).execute(team_id)

        assert len(result) == 2

    def test_wraps_repository_errors(self, repo):
        repo.get_keys_by_team_id.side_effect = Exception("boom")

        with pytest.raises(UserTeamsKeysRetrievalByTeamIdException):
            GetUserTeamsKeysByTeamIdUseCase(repo).execute(uuid.uuid4())


class TestGetUserTeamsKeysByUserIdUseCase:
    def test_maps_entities_to_dtos(self, repo):
        user_id = uuid.uuid4()
        keys = [make_key(user_id=user_id)]
        repo.get_keys_by_user_id.return_value = keys

        result = GetUserTeamsKeysByUserIdUseCase(repo).execute(user_id)

        assert len(result) == 1

    def test_wraps_repository_errors(self, repo):
        repo.get_keys_by_user_id.side_effect = Exception("boom")

        with pytest.raises(UserTeamsKeysRetrievalByUserIdException):
            GetUserTeamsKeysByUserIdUseCase(repo).execute(uuid.uuid4())


class TestUpdateUserTeamsKeyUseCase:
    def test_finds_matching_team_key_then_updates(self, repo):
        user_id, team_id = uuid.uuid4(), uuid.uuid4()
        existing = make_key(user_id=user_id, team_id=team_id, team_key_encrypted="old-key")
        other_team_key = make_key(user_id=user_id, team_id=uuid.uuid4(), team_key_encrypted="other-key")
        updated = make_key(id=existing.id, user_id=user_id, team_id=team_id, team_key_encrypted="new-key")
        repo.get_keys_by_user_id.return_value = [other_team_key, existing]
        repo.update_key.return_value = updated

        dto = UpdateUserTeamsKeyDTO(user_id=user_id, team_id=team_id, team_key_encrypted="new-key")
        result = UpdateUserTeamsKeyUseCase(repo).execute(uuid.uuid4(), dto)

        assert result.team_key_encrypted == "new-key"

    def test_raises_when_no_key_for_team(self, repo):
        user_id, team_id = uuid.uuid4(), uuid.uuid4()
        repo.get_keys_by_user_id.return_value = []

        dto = UpdateUserTeamsKeyDTO(user_id=user_id, team_id=team_id, team_key_encrypted="new-key")

        with pytest.raises(UserTeamsKeyUpdateException) as exc_info:
            UpdateUserTeamsKeyUseCase(repo).execute(uuid.uuid4(), dto)

        assert "not found" in str(exc_info.value).lower()

    def test_wraps_repository_errors(self, repo):
        repo.get_keys_by_user_id.side_effect = Exception("db error")
        dto = UpdateUserTeamsKeyDTO(user_id=uuid.uuid4(), team_id=uuid.uuid4(), team_key_encrypted="k")

        with pytest.raises(UserTeamsKeyUpdateException):
            UpdateUserTeamsKeyUseCase(repo).execute(uuid.uuid4(), dto)


class TestRemoveUserTeamsKeyUseCase:
    def test_returns_repository_result(self, repo):
        repo.remove_key.return_value = {"message": "Key removed successfully."}
        user_id, team_id = uuid.uuid4(), uuid.uuid4()

        result = RemoveUserTeamsKeyUseCase(repo).execute(uuid.uuid4(), RemoveUserTeamsKeyDTO(user_id=user_id, team_id=team_id))

        assert result == {"message": "Key removed successfully."}
        repo.remove_key.assert_called_once_with(user_id=user_id, team_id=team_id)

    def test_wraps_repository_errors(self, repo):
        repo.remove_key.side_effect = Exception("not found")

        with pytest.raises(UserTeamsKeyRemovalException):
            RemoveUserTeamsKeyUseCase(repo).execute(uuid.uuid4(), RemoveUserTeamsKeyDTO(user_id=uuid.uuid4(), team_id=uuid.uuid4()))
