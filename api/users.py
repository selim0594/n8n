from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional

from ..schemas.users import User, UserCreate, UserUpdateRole, UserCreateMultipleResponse
from ..services.users import UserService, get_user_service

router = APIRouter()


@router.get("/", response_model=List[User])
async def list_users(
    service: UserService = Depends(get_user_service),
    limit: int = Query(100, lte=250),
    include_role: bool = Query(False, alias="includeRole"),
    project_id: Optional[str] = Query(None, alias="projectId"),
):
    return await service.get_all(limit=limit, include_role=include_role, project_id=project_id)


@router.post("/", response_model=List[UserCreateMultipleResponse], status_code=status.HTTP_200_OK)
async def create_multiple_users(
    users_in: List[UserCreate], service: UserService = Depends(get_user_service)
):
    return await service.create_multiple(users_in)


@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: str,
    service: UserService = Depends(get_user_service),
    include_role: bool = Query(False, alias="includeRole"),
):
    user = await service.get_by_id(user_id, include_role=include_role)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, service: UserService = Depends(get_user_service)):
    success = await service.delete(user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.patch("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user_role(
    user_id: str,
    role_in: UserUpdateRole,
    service: UserService = Depends(get_user_service),
):
    success = await service.update_role(user_id, role_in)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"status": "success"}
