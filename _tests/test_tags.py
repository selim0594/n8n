import pytest
from unittest.mock import MagicMock
from fastapi import status

from ..services.tags import TagService
from ..schemas.tags import Tag, TagCreate


@pytest.mark.asyncio
async def test_get_all_tags(tag_service: TagService, mock_n8n_client: MagicMock):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": [
            {
                "id": "1",
                "name": "Test Tag",
                "createdAt": "2023-01-01T12:00:00.000Z",
                "updatedAt": "2023-01-01T12:00:00.000Z",
            }
        ]
    }
    mock_n8n_client.get_client().__aenter__.return_value.get.return_value = mock_response

    result = await tag_service.get_all()

    assert len(result) == 1
    assert isinstance(result[0], Tag)
    assert result[0].id == "1"
    mock_n8n_client.get_client().__aenter__.return_value.get.assert_called_once_with("/tags")


@pytest.mark.asyncio
async def test_create_tag(tag_service: TagService, mock_n8n_client: MagicMock):
    tag_data = TagCreate(name="New Tag")
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": "2",
        "name": "New Tag",
        "createdAt": "2023-01-02T12:00:00.000Z",
        "updatedAt": "2023-01-02T12:00:00.000Z",
    }
    mock_n8n_client.get_client().__aenter__.return_value.post.return_value = mock_response

    result = await tag_service.create(tag_data)

    assert isinstance(result, Tag)
    assert result.name == "New Tag"
    mock_n8n_client.get_client().__aenter__.return_value.post.assert_called_once()


@pytest.mark.asyncio
async def test_get_tag_by_id(tag_service: TagService, mock_n8n_client: MagicMock):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": "1",
        "name": "Test Tag",
        "createdAt": "2023-01-01T12:00:00.000Z",
        "updatedAt": "2023-01-01T12:00:00.000Z",
    }
    mock_n8n_client.get_client().__aenter__.return_value.get.return_value = mock_response

    result = await tag_service.get_by_id("1")

    assert isinstance(result, Tag)
    assert result.id == "1"
    mock_n8n_client.get_client().__aenter__.return_value.get.assert_called_once_with("/tags/1")


@pytest.mark.asyncio
async def test_delete_tag(tag_service: TagService, mock_n8n_client: MagicMock):
    mock_response = MagicMock()
    mock_response.status_code = status.HTTP_200_OK
    mock_n8n_client.get_client().__aenter__.return_value.delete.return_value = mock_response

    success = await tag_service.delete("1")

    assert success is True
    mock_n8n_client.get_client().__aenter__.return_value.delete.assert_called_once_with("/tags/1")
