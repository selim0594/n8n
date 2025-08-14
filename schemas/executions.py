from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from enum import Enum


class ExecutionStatus(str, Enum):
    WAITING = "waiting"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELED = "canceled"


class Execution(BaseModel):
    id: str
    status: ExecutionStatus
    workflow_id: str = Field(alias="workflowId")
    started_at: Optional[datetime] = Field(None, alias="startedAt")
    finished_at: Optional[datetime] = Field(None, alias="finishedAt")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
