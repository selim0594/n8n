from typing import List, Optional
from functools import lru_cache
from fastapi import status

from ..schemas.credentials import Credential, CredentialCreate, CredentialUpdate
from ..client import N8nClient, get_n8n_client


class CredentialService:
    def __init__(self, client: N8nClient):
        self.client = client

    async def get_all(self) -> List[Credential]:
        async with self.client.get_client() as http_client:
            response = await http_client.get("/credentials")
            response.raise_for_status()
            return [Credential.model_validate(item) for item in response.json().get("data", [])]

    async def get_by_id(self, credential_id: str) -> Optional[Credential]:
        async with self.client.get_client() as http_client:
            response = await http_client.get(f"/credentials/{credential_id}")
            if response.status_code == status.HTTP_404_NOT_FOUND:
                return None
            response.raise_for_status()
            return Credential.model_validate(response.json())

    async def create(self, credential_create: CredentialCreate) -> Credential:
        async with self.client.get_client() as http_client:
            response = await http_client.post(
                "/credentials",
                json=credential_create.model_dump(by_alias=True),
            )
            response.raise_for_status()
            return Credential.model_validate(response.json())

    async def update(
        self, credential_id: str, credential_update: CredentialUpdate
    ) -> Optional[Credential]:
        async with self.client.get_client() as http_client:
            response = await http_client.patch(
                f"/credentials/{credential_id}",
                json=credential_update.model_dump(by_alias=True, exclude_unset=True),
            )
            if response.status_code == status.HTTP_404_NOT_FOUND:
                return None
            response.raise_for_status()
            return Credential.model_validate(response.json())

    async def delete(self, credential_id: str) -> bool:
        async with self.client.get_client() as http_client:
            response = await http_client.delete(f"/credentials/{credential_id}")
            if response.status_code == status.HTTP_404_NOT_FOUND:
                return False
            response.raise_for_status()
            return response.status_code == status.HTTP_200_OK


@lru_cache
def get_credential_service(client: N8nClient = get_n8n_client()) -> CredentialService:
    return CredentialService(client)
