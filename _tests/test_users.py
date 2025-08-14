import pytest
from unittest.mock import MagicMock, AsyncMock
from ..services.users import UserService
from ..schemas.users import User, UserCreate, UserUpdateRole, UserRole, UserCreateMultipleResponse

USER_DATA_1 = {
    "id": "1",
    "email": "test1@example.com",
    "firstName": "Test",
    "lastName": "User1",
    "isPending": False,
    "createdAt": "2023-01-01T12:00:00.000Z",
    "updatedAt": "2023-01-01T12:00:00.000Z",
    "role": "global:member"
}

USER_DATA_2 = {
    "id": "2",
    "email": "test2@example.com",
    "firstName": "Another",
    "lastName": "User2",
    "isPending": True,
    "createdAt": "2023-01-02T12:00:00.000Z",
    "updatedAt": "2023-01-02T12:00:00.000Z",
    "role": "global:admin"
}

@pytest.fixture
def user_service(mock_n8n_client: MagicMock) -> UserService:
    return UserService(client=mock_n8n_client)

@pytest.mark.asyncio
async def test_get_all_users(user_service: UserService, mock_n8n_client: MagicMock):
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": [USER_DATA_1, USER_DATA_2]}
    mock_response.raise_for_status = MagicMock()
    
    mock_async_client = AsyncMock()
    mock_async_client.get.return_value = mock_response
    mock_n8n_client.get_client.return_value.__aenter__.return_value = mock_async_client

    result = await user_service.get_all()

    assert len(result) == 2
    assert isinstance(result[0], User)
    assert result[0].id == "1"
    assert result[1].email == "test2@example.com"
    mock_async_client.get.assert_called_once_with("/users", params={'limit': 100, 'includeRole': False, 'projectId': None})

@pytest.mark.asyncio
async def test_create_multiple_users(user_service: UserService, mock_n8n_client: MagicMock):
    users_to_create = [
        UserCreate(email="new1@example.com", role=UserRole.MEMBER),
        UserCreate(email="new2@example.com", role=UserRole.ADMIN)
    ]
    mock_response_data = [
        {"user": {"id": "3", "email": "new1@example.com"}},
        {"error": "User already exists"}
    ]
    mock_response = MagicMock()
    mock_response.json.return_value = mock_response_data
    mock_response.raise_for_status = MagicMock()

    mock_async_client = AsyncMock()
    mock_async_client.post.return_value = mock_response
    mock_n8n_client.get_client.return_value.__aenter__.return_value = mock_async_client

    result = await user_service.create_multiple(users_to_create)

    assert len(result) == 2
    assert isinstance(result[0], UserCreateMultipleResponse)
    assert result[0].user["email"] == "new1@example.com"
    assert result[1].error == "User already exists"
    
    expected_payload = [
        {'email': 'new1@example.com', 'role': 'global:member'},
        {'email': 'new2@example.com', 'role': 'global:admin'}
    ]
    mock_async_client.post.assert_called_once_with("/users", json=expected_payload)


@pytest.mark.asyncio
async def test_get_user_by_id(user_service: UserService, mock_n8n_client: MagicMock):
    mock_response = MagicMock()
    mock_response.json.return_value = USER_DATA_1
    mock_response.raise_for_status = MagicMock()
    mock_response.status_code = 200

    mock_async_client = AsyncMock()
    mock_async_client.get.return_value = mock_response
    mock_n8n_client.get_client.return_value.__aenter__.return_value = mock_async_client

    result = await user_service.get_by_id("1", include_role=True)

    assert isinstance(result, User)
    assert result.id == "1"
    assert result.email == "test1@example.com"
    mock_async_client.get.assert_called_once_with("/users/1", params={'includeRole': True})

@pytest.mark.asyncio
async def test_delete_user(user_service: UserService, mock_n8n_client: MagicMock):
    mock_response = MagicMock()
    mock_response.status_code = 204
    mock_response.raise_for_status = MagicMock()

    mock_async_client = AsyncMock()
    mock_async_client.delete.return_value = mock_response
    mock_n8n_client.get_client.return_value.__aenter__.return_value = mock_async_client

    result = await user_service.delete("1")

    assert result is True
    mock_async_client.delete.assert_called_once_with("/users/1")

@pytest.mark.asyncio
async def test_update_user_role(user_service: UserService, mock_n8n_client: MagicMock):
    role_update = UserUpdateRole(new_role_name=UserRole.ADMIN)
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.raise_for_status = MagicMock()

    mock_async_client = AsyncMock()
    mock_async_client.patch.return_value = mock_response
    mock_n8n_client.get_client.return_value.__aenter__.return_value = mock_async_client

    result = await user_service.update_role("1", role_update)

    assert result is True
    expected_payload = {'newRoleName': 'global:admin'}
    mock_async_client.patch.assert_called_once_with("/users/1", json=expected_payload)
