from typing import List, Optional
from fastapi import HTTPException, status
from functools import lru_cache

from ..schemas.users import User, UserCreate, UserUpdate
from ..client import N8nClient, get_n8n_client


class UserService:
    def __init__(self, client: N8nClient):
        self.client = client

    async def get_all(self) -> List[User]:
        async with self.client.get_client() as http_client:
            response = await http_client.get("/users")
            response.raise_for_status()
            return [User.model_validate(item) for item in response.json().get("data", [])]

    async def get_by_id(self, user_id: str) -> Optional[User]:
        async with self.client.get_client() as http_client:
            response = await http_client.get(f"/users/{user_id}")
            if response.status_code == status.HTTP_404_NOT_FOUND:
                return None
            response.raise_for_status()
            return User.model_validate(response.json())

    async def create(self, user_create: UserCreate) -> User:
        async with self.client.get_client() as http_client:
            response = await http_client.post(
                "/users",
                json=user_create.model_dump(by_alias=True),
            )
            response.raise_for_status()
            return User.model_validate(response.json())

    async def update(self, user_id: str, user_update: UserUpdate) -> Optional[User]:
        async with self.client.get_client() as http_client:
            response = await http_client.patch(
                f"/users/{user_id}",
                json=user_update.model_dump(by_alias=True, exclude_unset=True),
            )
            if response.status_code == status.HTTP_404_NOT_FOUND:
                return None
            response.raise_for_status()
            return User.model_validate(response.json())

    async def delete(self, user_id: str) -> bool:
        async with self.client.get_client() as http_client:
            response = await http_client.delete(f"/users/{user_id}")
            if response.status_code == status.HTTP_404_NOT_FOUND:
                return False
            response.raise_for_status()
            return response.status_code == status.HTTP_200_OK


@lru_cache
def get_user_service(client: N8nClient = get_n8n_client()) -> UserService:
    return UserService(client)
