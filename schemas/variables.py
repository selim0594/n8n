from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Any


class VariableCreate(BaseModel):
    name: str
    value: Any


class VariableUpdate(BaseModel):
    name: str
    value: Any


class Variable(BaseModel):
    id: str
    name: str
    value: Any
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
