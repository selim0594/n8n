from typing import List, Optional
from functools import lru_cache
from fastapi import status

from ..schemas.tags import Tag, TagCreate, TagUpdate
from ..client import N8nClient, get_n8n_client


class TagService:
    def __init__(self, client: N8nClient):
        self.client = client

    async def get_all(self) -> List[Tag]:
        async with self.client.get_client() as http_client:
            response = await http_client.get("/tags")
            response.raise_for_status()
            return [Tag.model_validate(item) for item in response.json().get("data", [])]

    async def get_by_id(self, tag_id: str) -> Optional[Tag]:
        async with self.client.get_client() as http_client:
            response = await http_client.get(f"/tags/{tag_id}")
            if response.status_code == status.HTTP_404_NOT_FOUND:
                return None
            response.raise_for_status()
            return Tag.model_validate(response.json())

    async def create(self, tag_create: TagCreate) -> Tag:
        async with self.client.get_client() as http_client:
            response = await http_client.post(
                "/tags",
                json=tag_create.model_dump(by_alias=True),
            )
            response.raise_for_status()
            return Tag.model_validate(response.json())

    async def update(self, tag_id: str, tag_update: TagUpdate) -> Optional[Tag]:
        async with self.client.get_client() as http_client:
            response = await http_client.put(
                f"/tags/{tag_id}",
                json=tag_update.model_dump(by_alias=True),
            )
            if response.status_code == status.HTTP_404_NOT_FOUND:
                return None
            response.raise_for_status()
            return Tag.model_validate(response.json())

    async def delete(self, tag_id: str) -> bool:
        async with self.client.get_client() as http_client:
            response = await http_client.delete(f"/tags/{tag_id}")
            if response.status_code == status.HTTP_404_NOT_FOUND:
                return False
            response.raise_for_status()
            return response.status_code == status.HTTP_200_OK


@lru_cache
def get_tag_service(client: N8nClient = get_n8n_client()) -> TagService:
    return TagService(client)
