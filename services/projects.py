from typing import List
from functools import lru_cache

from ..schemas.projects import Project
from ..client import N8nClient, get_n8n_client


class ProjectService:
    def __init__(self, client: N8nClient):
        self.client = client

    async def get_all(self) -> List[Project]:
        async with self.client.get_client() as http_client:
            response = await http_client.get("/projects")
            response.raise_for_status()
            return [Project.model_validate(item) for item in response.json()]


@lru_cache
def get_project_service(client: N8nClient = get_n8n_client()) -> ProjectService:
    return ProjectService(client)
