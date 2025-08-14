import pytest
from unittest.mock import MagicMock
from fastapi import status

from ..services.variables import VariableService
from ..schemas.variables import Variable, VariableCreate


@pytest.mark.asyncio
async def test_get_all_variables(variable_service: VariableService, mock_n8n_client: MagicMock):
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {
            "id": "1",
            "name": "Test Variable",
            "value": "test_value",
            "createdAt": "2023-01-01T12:00:00.000Z",
            "updatedAt": "2023-01-01T12:00:00.000Z",
        }
    ]
    mock_n8n_client.get_client().__aenter__.return_value.get.return_value = mock_response

    result = await variable_service.get_all()

    assert len(result) == 1
    assert isinstance(result[0], Variable)
    assert result[0].id == "1"
    mock_n8n_client.get_client().__aenter__.return_value.get.assert_called_once_with("/variables")


@pytest.mark.asyncio
async def test_create_variable(variable_service: VariableService, mock_n8n_client: MagicMock):
    variable_data = VariableCreate(name="New Variable", value="new_value")
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": "2",
        "name": "New Variable",
        "value": "new_value",
        "createdAt": "2023-01-02T12:00:00.000Z",
        "updatedAt": "2023-01-02T12:00:00.000Z",
    }
    mock_n8n_client.get_client().__aenter__.return_value.post.return_value = mock_response

    result = await variable_service.create(variable_data)

    assert isinstance(result, Variable)
    assert result.name == "New Variable"
    mock_n8n_client.get_client().__aenter__.return_value.post.assert_called_once()


@pytest.mark.asyncio
async def test_get_variable_by_id(variable_service: VariableService, mock_n8n_client: MagicMock):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": "1",
        "name": "Test Variable",
        "value": "test_value",
        "createdAt": "2023-01-01T12:00:00.000Z",
        "updatedAt": "2023-01-01T12:00:00.000Z",
    }
    mock_n8n_client.get_client().__aenter__.return_value.get.return_value = mock_response

    result = await variable_service.get_by_id("1")

    assert isinstance(result, Variable)
    assert result.id == "1"
    mock_n8n_client.get_client().__aenter__.return_value.get.assert_called_once_with("/variables/1")


@pytest.mark.asyncio
async def test_delete_variable(variable_service: VariableService, mock_n8n_client: MagicMock):
    mock_response = MagicMock()
    mock_response.status_code = status.HTTP_204_NO_CONTENT
    mock_n8n_client.get_client().__aenter__.return_value.delete.return_value = mock_response

    success = await variable_service.delete("1")

    assert success is True
    mock_n8n_client.get_client().__aenter__.return_value.delete.assert_called_once_with("/variables/1")
