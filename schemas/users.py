from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    first_name: str = Field(alias='firstName')
    last_name: str = Field(alias='lastName')
    email: EmailStr
    language: Optional[str] = None
    global_role: Optional[str] = Field(None, alias='globalRole')

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, alias='firstName')
    last_name: Optional[str] = Field(None, alias='lastName')
    email: Optional[EmailStr] = None
    language: Optional[str] = None
    password: Optional[str] = None
    global_role: Optional[str] = Field(None, alias='globalRole')

class User(UserBase):
    id: str
    created_at: datetime = Field(alias='createdAt')
    updated_at: datetime = Field(alias='updatedAt')

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
