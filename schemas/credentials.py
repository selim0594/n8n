from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Any, Optional
from datetime import datetime


class CredentialCreate(BaseModel):
    name: str
    type: str
    data: Dict[str, Any]


class CredentialUpdate(BaseModel):
    name: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


class Credential(BaseModel):
    id: str
    name: str
    type: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
