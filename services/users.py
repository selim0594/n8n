from typing import List, Optional
from fastapi import HTTPException, status
from functools import lru_cache

from ..schemas.users import User, UserCreate, UserUpdateRole, UserCreateMultipleResponse
from ..client import N8nClient, get_n8n_client


class UserService:
    def __init__(self, client: N8nClient):
        self.client = client

    async def get_all(self, limit: int = 100, include_role: bool = False, project_id: Optional[str] = None) -> List[User]:
        params = {"limit": limit, "includeRole": include_role}
        if project_id:
            params["projectId"] = project_id
        
        async with self.client.get_client() as http_client:
            response = await http_client.get("/users", params=params)
            response.raise_for_status()
            return [User.model_validate(item) for item in response.json().get("data", [])]

    async def create_multiple(self, users: List[UserCreate]) -> List[UserCreateMultipleResponse]:
        async with self.client.get_client() as http_client:
            response = await http_client.post("/users", json=[user.model_dump(by_alias=True) for user in users])
            response.raise_for_status()
            return [UserCreateMultipleResponse.model_validate(item) for item in response.json()]

    async def get_by_id(self, user_id: str, include_role: bool = False) -> Optional[User]:
        params = {"includeRole": include_role}
        async with self.client.get_client() as http_client:
            response = await http_client.get(f"/users/{user_id}", params=params)
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
            return response.status_code == status.HTTP_204_NO_CONTENT

    async def update_role(self, user_id: str, role_update: UserUpdateRole) -> bool:
        async with self.client.get_client() as http_client:
            response = await http_client.patch(
                f"/users/{user_id}",
                json=role_update.model_dump(by_alias=True),
            )
            response.raise_for_status()
            return response.status_code == status.HTTP_200_OK


@lru_cache
def get_user_service(client: N8nClient = get_n8n_client()) -> UserService:
    return UserService(client)
