from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any, Optional
from datetime import datetime


class Tag(BaseModel):
    id: str
    name: str
    created_at: datetime = Field(alias='createdAt')
    updated_at: datetime = Field(alias='updatedAt')

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class WorkflowBase(BaseModel):
    name: str
    active: bool = False
    nodes: List[Dict[str, Any]] = []
    connections: Dict[str, Any] = {}
    settings: Optional[Dict[str, Any]] = None
    static_data: Optional[str] = Field(None, alias='staticData')
    tags: List[Tag] = []


class WorkflowCreate(WorkflowBase):
    pass


class WorkflowUpdate(WorkflowBase):
    pass


class Workflow(WorkflowBase):
    id: str
    created_at: datetime = Field(alias='createdAt')
    updated_at: datetime = Field(alias='updatedAt')

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
