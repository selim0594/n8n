from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class SourceControlPullOptions(BaseModel):
    force: bool = False
    variables: Optional[Dict[str, Any]] = None


class SourceControlVariableChanges(BaseModel):
    added: List[str]
    changed: List[str]


class SourceControlTagChanges(BaseModel):
    tags: List[Dict[str, Any]]
    mappings: List[Dict[str, Any]]


class SourceControlPullResult(BaseModel):
    variables: SourceControlVariableChanges
    credentials: List[Dict[str, Any]]
    workflows: List[Dict[str, Any]]
    tags: SourceControlTagChanges
