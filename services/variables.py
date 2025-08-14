from typing import List, Optional, Any
from functools import lru_cache
from fastapi import status

from ..schemas.variables import Variable, VariableCreate, VariableUpdate
from ..client import N8nClient, get_n8n_client


class VariableService:
    def __init__(self, client: N8nClient):
        self.client = client

    async def get_all(self) -> List[Variable]:
        async with self.client.get_client() as http_client:
            response = await http_client.get("/variables")
            response.raise_for_status()
            return [Variable.model_validate(item) for item in response.json()]

    async def get_by_id(self, variable_id: str) -> Optional[Variable]:
        async with self.client.get_client() as http_client:
            response = await http_client.get(f"/variables/{variable_id}")
            if response.status_code == status.HTTP_404_NOT_FOUND:
                return None
            response.raise_for_status()
            return Variable.model_validate(response.json())

    async def create(self, variable_create: VariableCreate) -> Variable:
        async with self.client.get_client() as http_client:
            response = await http_client.post(
                "/variables",
                json=variable_create.model_dump(by_alias=True),
            )
            response.raise_for_status()
            return Variable.model_validate(response.json())

    async def update(self, variable_id: str, variable_update: VariableUpdate) -> Optional[Variable]:
        async with self.client.get_client() as http_client:
            response = await http_client.put(
                f"/variables/{variable_id}",
                json=variable_update.model_dump(by_alias=True),
            )
            if response.status_code == status.HTTP_404_NOT_FOUND:
                return None
            response.raise_for_status()
            return Variable.model_validate(response.json())

    async def delete(self, variable_id: str) -> bool:
        async with self.client.get_client() as http_client:
            response = await http_client.delete(f"/variables/{variable_id}")
            if response.status_code == status.HTTP_404_NOT_FOUND:
                return False
            response.raise_for_status()
            return response.status_code == status.HTTP_204_NO_CONTENT


@lru_cache
def get_variable_service(client: N8nClient = get_n8n_client()) -> VariableService:
    return VariableService(client)
