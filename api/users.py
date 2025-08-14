from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from ..schemas.users import User, UserCreate, UserUpdate
from ..services.users import UserService, get_user_service

router = APIRouter()


@router.get("/", response_model=List[User])
async def list_users(service: UserService = Depends(get_user_service)):
    return await service.get_all()


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, service: UserService = Depends(get_user_service)):
    return await service.create(user_in)


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str, service: UserService = Depends(get_user_service)):
    user = await service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=User)
async def update_user(
    user_id: str, user_in: UserUpdate, service: UserService = Depends(get_user_service)
):
    user = await service.update(user_id, user_in)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, service: UserService = Depends(get_user_service)):
    success = await service.delete(user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
