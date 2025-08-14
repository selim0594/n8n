from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Any
from ..schemas.workflows import Workflow, WorkflowCreate, WorkflowUpdate
from ..services.workflows import WorkflowService, get_workflow_service

router = APIRouter()


@router.get("/", response_model=List[Workflow])
async def list_workflows(service: WorkflowService = Depends(get_workflow_service)):
    return await service.get_all()


@router.post("/", response_model=Workflow, status_code=status.HTTP_201_CREATED)
async def create_workflow(
    workflow_in: WorkflowCreate, service: WorkflowService = Depends(get_workflow_service)
):
    return await service.create(workflow_in)


@router.get("/{workflow_id}", response_model=Workflow)
async def get_workflow(
    workflow_id: str, service: WorkflowService = Depends(get_workflow_service)
):
    workflow = await service.get_by_id(workflow_id)
    if not workflow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")
    return workflow


@router.put("/{workflow_id}", response_model=Workflow)
async def update_workflow(
    workflow_id: str,
    workflow_in: WorkflowUpdate,
    service: WorkflowService = Depends(get_workflow_service),
):
    workflow = await service.update(workflow_id, workflow_in)
    if not workflow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")
    return workflow


@router.delete("/{workflow_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workflow(
    workflow_id: str, service: WorkflowService = Depends(get_workflow_service)
):
    success = await service.delete(workflow_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")


@router.post("/{workflow_id}/activate", response_model=dict)
async def activate_workflow(
    workflow_id: str, service: WorkflowService = Depends(get_workflow_service)
):
    try:
        return await service.activate(workflow_id)
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")
        raise e


@router.post("/{workflow_id}/deactivate", response_model=dict)
async def deactivate_workflow(
    workflow_id: str, service: WorkflowService = Depends(get_workflow_service)
):
    try:
        return await service.deactivate(workflow_id)
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")
        raise e
