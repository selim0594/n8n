import pytest
from unittest.mock import MagicMock

from ..services.projects import ProjectService
from ..schemas.projects import Project


@pytest.mark.asyncio
async def test_get_all_projects(project_service: ProjectService, mock_n8n_client: MagicMock):
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {
            "id": "1",
            "name": "Test Project",
            "createdAt": "2023-01-01T12:00:00.000Z",
            "updatedAt": "2023-01-01T12:00:00.000Z",
        }
    ]
    mock_n8n_client.get_client().__aenter__.return_value.get.return_value = mock_response

    result = await project_service.get_all()

    assert len(result) == 1
    assert isinstance(result[0], Project)
    assert result[0].id == "1"
    mock_n8n_client.get_client().__aenter__.return_value.get.assert_called_once_with("/projects")
