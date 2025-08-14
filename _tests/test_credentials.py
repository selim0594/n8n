import pytest
from unittest.mock import MagicMock
from fastapi import status

from ..services.credentials import CredentialService
from ..schemas.credentials import Credential, CredentialCreate


@pytest.mark.asyncio
async def test_get_all_credentials(credential_service: CredentialService, mock_n8n_client: MagicMock):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": [
            {
                "id": "1",
                "name": "Test Credential",
                "type": "test_type",
                "createdAt": "2023-01-01T12:00:00.000Z",
                "updatedAt": "2023-01-01T12:00:00.000Z",
            }
        ]
    }
    mock_n8n_client.get_client().__aenter__.return_value.get.return_value = mock_response

    result = await credential_service.get_all()

    assert len(result) == 1
    assert isinstance(result[0], Credential)
    assert result[0].id == "1"
    mock_n8n_client.get_client().__aenter__.return_value.get.assert_called_once_with("/credentials")


@pytest.mark.asyncio
async def test_create_credential(credential_service: CredentialService, mock_n8n_client: MagicMock):
    credential_data = CredentialCreate(name="New Credential", type="new_type", data={})
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": "2",
        "name": "New Credential",
        "type": "new_type",
        "createdAt": "2023-01-02T12:00:00.000Z",
        "updatedAt": "2023-01-02T12:00:00.000Z",
    }
    mock_n8n_client.get_client().__aenter__.return_value.post.return_value = mock_response

    result = await credential_service.create(credential_data)

    assert isinstance(result, Credential)
    assert result.name == "New Credential"
    mock_n8n_client.get_client().__aenter__.return_value.post.assert_called_once()


@pytest.mark.asyncio
async def test_get_credential_by_id(credential_service: CredentialService, mock_n8n_client: MagicMock):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": "1",
        "name": "Test Credential",
        "type": "test_type",
        "createdAt": "2023-01-01T12:00:00.000Z",
        "updatedAt": "2023-01-01T12:00:00.000Z",
    }
    mock_n8n_client.get_client().__aenter__.return_value.get.return_value = mock_response

    result = await credential_service.get_by_id("1")

    assert isinstance(result, Credential)
    assert result.id == "1"
    mock_n8n_client.get_client().__aenter__.return_value.get.assert_called_once_with("/credentials/1")


@pytest.mark.asyncio
async def test_delete_credential(credential_service: CredentialService, mock_n8n_client: MagicMock):
    mock_response = MagicMock()
    mock_response.status_code = status.HTTP_200_OK
    mock_n8n_client.get_client().__aenter__.return_value.delete.return_value = mock_response

    success = await credential_service.delete("1")

    assert success is True
    mock_n8n_client.get_client().__aenter__.return_value.delete.assert_called_once_with("/credentials/1")
