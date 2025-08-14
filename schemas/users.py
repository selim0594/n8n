from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "global:admin"
    MEMBER = "global:member"


class User(BaseModel):
    id: str
    email: EmailStr
    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")
    is_pending: Optional[bool] = Field(None, alias="isPending")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    role: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class UserCreate(BaseModel):
    email: EmailStr
    role: Optional[UserRole] = None


class UserCreateMultipleResponse(BaseModel):
    user: Optional[dict] = None
    error: Optional[str] = None


class UserUpdateRole(BaseModel):
    new_role_name: UserRole = Field(..., alias="newRoleName")

    model_config = ConfigDict(populate_by_name=True)
