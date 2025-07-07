import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from uuid import uuid4
from mainApp import app

client = TestClient(app)

@pytest.fixture
def container_mock():
    container = app.container
    container.local_user = MagicMock()
    container.local_user().CreateLocalUserProvider.return_value = MagicMock()
    container.local_user().GetAllLocalUsersByMainUserIdProvider.return_value = MagicMock()
    container.local_user().UpdateLocalUserByIdProvider.return_value = MagicMock()
    container.local_user().DeleteLocalUserByIdProvider.return_value = MagicMock()
    yield container
    container.local_user.reset_mock()


def test_create_user_success(container_mock):
    fakeUser = {"id": str(uuid4()), "username": "Mario"}
    usecase_mock = container_mock.local_user().CreateLocalUserProvider.return_value
    usecase_mock.execute.return_value = fakeUser

    payload = {"username": "Mario", "email": "mario@example.com", "password": "Pass123"}

    response = client.post("/api/V1/localuser/", json=payload)

    assert response.status_code == 200
    assert response.json()["user"] == fakeUser
    usecase_mock.execute.assert_called_once()
    
# Altri test per GET, PUT, DELETE come ti ho mostrato prima...
