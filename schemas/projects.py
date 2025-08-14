from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class Project(BaseModel):
    id: str
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
