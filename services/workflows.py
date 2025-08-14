from typing import List, Optional
from fastapi import HTTPException, status
from functools import lru_cache

from ..schemas.workflows import Workflow, WorkflowCreate, WorkflowUpdate
from ..client import N8nClient, get_n8n_client


class WorkflowService:
    def __init__(self, client: N8nClient):
        self.client = client

    async def get_all(self) -> List[Workflow]:
        async with self.client.get_client() as http_client:
            response = await http_client.get("/workflows")
            response.raise_for_status()
            return [Workflow.model_validate(item) for item in response.json().get("data", [])]

    async def get_by_id(self, workflow_id: str) -> Optional[Workflow]:
        async with self.client.get_client() as http_client:
            response = await http_client.get(f"/workflows/{workflow_id}")
            if response.status_code == status.HTTP_404_NOT_FOUND:
                return None
            response.raise_for_status()
            return Workflow.model_validate(response.json())

    async def create(self, workflow_create: WorkflowCreate) -> Workflow:
        async with self.client.get_client() as http_client:
            response = await http_client.post(
                "/workflows",
                json=workflow_create.model_dump(by_alias=True, exclude_unset=True),
            )
            response.raise_for_status()
            return Workflow.model_validate(response.json())

    async def update(self, workflow_id: str, workflow_update: WorkflowUpdate) -> Optional[Workflow]:
        async with self.client.get_client() as http_client:
            response = await http_client.put(
                f"/workflows/{workflow_id}",
                json=workflow_update.model_dump(by_alias=True, exclude_unset=True),
            )
            if response.status_code == status.HTTP_404_NOT_FOUND:
                return None
            response.raise_for_status()
            return Workflow.model_validate(response.json())

    async def delete(self, workflow_id: str) -> bool:
        async with self.client.get_client() as http_client:
            response = await http_client.delete(f"/workflows/{workflow_id}")
            if response.status_code == status.HTTP_404_NOT_FOUND:
                return False
            response.raise_for_status()
            return response.status_code == status.HTTP_200_OK

    async def activate(self, workflow_id: str) -> dict:
        async with self.client.get_client() as http_client:
            response = await http_client.post(f"/workflows/{workflow_id}/activate")
            response.raise_for_status()
            return response.json()

    async def deactivate(self, workflow_id: str) -> dict:
        async with self.client.get_client() as http_client:
            response = await http_client.post(f"/workflows/{workflow_id}/deactivate")
            response.raise_for_status()
            return response.json()


@lru_cache
def get_workflow_service(client: N8nClient = get_n8n_client()) -> WorkflowService:
    return WorkflowService(client)
