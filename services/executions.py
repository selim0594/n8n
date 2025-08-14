from typing import List, Optional
from functools import lru_cache
from fastapi import status

from ..schemas.executions import Execution
from ..client import N8nClient, get_n8n_client


class ExecutionService:
    def __init__(self, client: N8nClient):
        self.client = client

    async def get_all(self) -> List[Execution]:
        async with self.client.get_client() as http_client:
            response = await http_client.get("/executions")
            response.raise_for_status()
            # The n8n API returns a dictionary with a 'data' key containing the list
            return [Execution.model_validate(item) for item in response.json().get("data", [])]

    async def get_by_id(self, execution_id: str) -> Optional[Execution]:
        async with self.client.get_client() as http_client:
            response = await http_client.get(f"/executions/{execution_id}")
            if response.status_code == status.HTTP_404_NOT_FOUND:
                return None
            response.raise_for_status()
            return Execution.model_validate(response.json())

    async def delete(self, execution_id: str) -> bool:
        async with self.client.get_client() as http_client:
            response = await http_client.delete(f"/executions/{execution_id}")
            if response.status_code == status.HTTP_404_NOT_FOUND:
                return False
            response.raise_for_status()
            # A successful deletion returns a 200 OK with a success message
            return response.status_code == status.HTTP_200_OK


@lru_cache
def get_execution_service(client: N8nClient = get_n8n_client()) -> ExecutionService:
    return ExecutionService(client)
