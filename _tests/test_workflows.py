import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime

from ..services.workflows import WorkflowService
from ..schemas.workflows import Workflow, WorkflowCreate, WorkflowUpdate


@pytest.mark.asyncio
async def test_get_all_workflows(workflow_service: WorkflowService, mock_n8n_client: MagicMock):
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {
            "id": "1",
            "name": "Test Workflow 1",
            "active": True,
            "nodes": [],
            "connections": {},
            "createdAt": "2023-01-01T12:00:00.000Z",
            "updatedAt": "2023-01-01T12:00:00.000Z",
        }
    ]
    mock_n8n_client.get_client().__aenter__.return_value.get.return_value = mock_response

    result = await workflow_service.get_all()

    assert len(result) == 1
    assert isinstance(result[0], Workflow)
    assert result[0].id == "1"
    mock_n8n_client.get_client().__aenter__.return_value.get.assert_called_once_with("/workflows")


@pytest.mark.asyncio
async def test_create_workflow(workflow_service: WorkflowService, mock_n8n_client: MagicMock):
    workflow_data = WorkflowCreate(name="New Workflow", nodes=[{"type": "test", "typeVersion": 1, "parameters": {}}], connections={}, active=False)
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": "2",
        "name": "New Workflow",
        "active": False,
        "nodes": [],
        "connections": {},
        "createdAt": "2023-01-02T12:00:00.000Z",
        "updatedAt": "2023-01-02T12:00:00.000Z",
    }
    mock_n8n_client.get_client().__aenter__.return_value.post.return_value = mock_response

    result = await workflow_service.create(workflow_data)

    assert isinstance(result, Workflow)
    assert result.name == "New Workflow"
    mock_n8n_client.get_client().__aenter__.return_value.post.assert_called_once()


@pytest.mark.asyncio
async def test_get_workflow_by_id(workflow_service: WorkflowService, mock_n8n_client: MagicMock):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": "1",
        "name": "Test Workflow",
        "active": True,
        "nodes": [],
        "connections": {},
        "createdAt": "2023-01-01T12:00:00.000Z",
        "updatedAt": "2023-01-01T12:00:00.000Z",
    }
    mock_n8n_client.get_client().__aenter__.return_value.get.return_value = mock_response

    result = await workflow_service.get_by_id("1")

    assert isinstance(result, Workflow)
    assert result.id == "1"
    mock_n8n_client.get_client().__aenter__.return_value.get.assert_called_once_with("/workflows/1")


@pytest.mark.asyncio
async def test_update_workflow(workflow_service: WorkflowService, mock_n8n_client: MagicMock):
    update_data = WorkflowUpdate(name="Updated Workflow")
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": "1",
        "name": "Updated Workflow",
        "active": True,
        "nodes": [],
        "connections": {},
        "createdAt": "2023-01-01T12:00:00.000Z",
        "updatedAt": "2023-01-03T12:00:00.000Z",
    }
    mock_n8n_client.get_client().__aenter__.return_value.put.return_value = mock_response

    result = await workflow_service.update("1", update_data)

    assert isinstance(result, Workflow)
    assert result.name == "Updated Workflow"
    mock_n8n_client.get_client().__aenter__.return_value.put.assert_called_once()


@pytest.mark.asyncio
async def test_delete_workflow(workflow_service: WorkflowService, mock_n8n_client: MagicMock):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_n8n_client.get_client().__aenter__.return_value.delete.return_value = mock_response

    success = await workflow_service.delete("1")

    assert success is True
    mock_n8n_client.get_client().__aenter__.return_value.delete.assert_called_once_with("/workflows/1")
