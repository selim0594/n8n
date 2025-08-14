import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import status

from ..services.executions import ExecutionService
from ..schemas.executions import Execution, ExecutionStatus


@pytest.mark.asyncio
async def test_get_all_executions(execution_service: ExecutionService, mock_n8n_client: MagicMock):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": [
            {
                "id": "1",
                "status": "success",
                "startedAt": "2023-01-01T12:00:00.000Z",
                "stoppedAt": "2023-01-01T12:01:00.000Z",
                "workflowId": "w1"
            }
        ]
    }
    mock_n8n_client.get_client().__aenter__.return_value.get.return_value = mock_response

    result = await execution_service.get_all()

    assert len(result) == 1
    assert isinstance(result[0], Execution)
    assert result[0].status == ExecutionStatus.SUCCESS
    mock_n8n_client.get_client().__aenter__.return_value.get.assert_called_once_with("/executions")


@pytest.mark.asyncio
async def test_get_execution_by_id(execution_service: ExecutionService, mock_n8n_client: MagicMock):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": "1",
        "status": "success",
        "startedAt": "2023-01-01T12:00:00.000Z",
        "stoppedAt": "2023-01-01T12:01:00.000Z",
        "workflowId": "w1"
    }
    mock_n8n_client.get_client().__aenter__.return_value.get.return_value = mock_response

    result = await execution_service.get_by_id("1")

    assert isinstance(result, Execution)
    assert result.id == "1"
    mock_n8n_client.get_client().__aenter__.return_value.get.assert_called_once_with("/executions/1")


@pytest.mark.asyncio
async def test_delete_execution(execution_service: ExecutionService, mock_n8n_client: MagicMock):
    mock_response = MagicMock()
    mock_response.status_code = status.HTTP_200_OK
    mock_n8n_client.get_client().__aenter__.return_value.delete.return_value = mock_response

    success = await execution_service.delete("1")

    assert success is True
    mock_n8n_client.get_client().__aenter__.return_value.delete.assert_called_once_with("/executions/1")
