from fastapi import APIRouter, Depends, Body
from typing import Optional

from ..schemas.source_control import SourceControlPullResult, SourceControlPullOptions
from ..services.source_control import SourceControlService, get_source_control_service

router = APIRouter()


@router.post("/pull", response_model=SourceControlPullResult)
async def pull_from_repository(
    options: Optional[SourceControlPullOptions] = Body(None),
    service: SourceControlService = Depends(get_source_control_service),
) -> SourceControlPullResult:
    return await service.pull(options=options)
