from fastapi import APIRouter, Depends
from typing import List

from ..schemas.projects import Project
from ..services.projects import ProjectService, get_project_service

router = APIRouter()


@router.get("/", response_model=List[Project])
async def list_projects(service: ProjectService = Depends(get_project_service)):
    return await service.get_all()
