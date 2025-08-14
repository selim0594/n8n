import pytest
from unittest.mock import MagicMock

from ..services.users import UserService
from ..schemas.users import User


@pytest.mark.asyncio
async def test_get_all_users(user_service: UserService, mock_n8n_client: MagicMock):
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {
            "id": "1",
            "firstName": "Test",
            "lastName": "User",
            "email": "test@example.com",
            "createdAt": "2023-01-01T12:00:00.000Z",
            "updatedAt": "2023-01-01T12:00:00.000Z",
        }
    ]
    mock_n8n_client.get_client().__aenter__.return_value.get.return_value = mock_response

    result = await user_service.get_all()

    assert len(result) == 1
    assert isinstance(result[0], User)
    assert result[0].id == "1"
    mock_n8n_client.get_client().__aenter__.return_value.get.assert_called_once_with("/users")


@pytest.mark.asyncio
async def test_get_user_by_id(user_service: UserService, mock_n8n_client: MagicMock):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": "1",
        "firstName": "Test",
        "lastName": "User",
        "email": "test@example.com",
        "createdAt": "2023-01-01T12:00:00.000Z",
        "updatedAt": "2023-01-01T12:00:00.000Z",
    }
    mock_n8n_client.get_client().__aenter__.return_value.get.return_value = mock_response

    result = await user_service.get_by_id("1")

    assert isinstance(result, User)
    assert result.id == "1"
    mock_n8n_client.get_client().__aenter__.return_value.get.assert_called_once_with("/users/1")
