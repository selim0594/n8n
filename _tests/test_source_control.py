import pytest
from unittest.mock import MagicMock

from ..services.source_control import SourceControlService
from ..schemas.source_control import SourceControlPullResult, SourceControlPullOptions


@pytest.mark.asyncio
async def test_pull_from_repository(source_control_service: SourceControlService, mock_n8n_client: MagicMock):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "variables": {"added": [], "changed": []},
        "credentials": [],
        "workflows": [],
        "tags": {"tags": [], "mappings": []},
    }
    mock_n8n_client.get_client().__aenter__.return_value.post.return_value = mock_response

    options = SourceControlPullOptions(force=True)
    result = await source_control_service.pull(options)

    assert isinstance(result, SourceControlPullResult)
    assert result.variables.added == []
    mock_n8n_client.get_client().__aenter__.return_value.post.assert_called_once_with(
        "/source-control/pull",
        json={"force": True}
    )
