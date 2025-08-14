from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from ..schemas.executions import Execution
from ..services.executions import ExecutionService, get_execution_service

router = APIRouter()


@router.get("/", response_model=List[Execution])
async def list_executions(service: ExecutionService = Depends(get_execution_service)):
    return await service.get_all()


@router.get("/{execution_id}", response_model=Execution)
async def get_execution(
    execution_id: str, service: ExecutionService = Depends(get_execution_service)
):
    execution = await service.get_by_id(execution_id)
    if not execution:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Execution not found")
    return execution


@router.delete("/{execution_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_execution(
    execution_id: str, service: ExecutionService = Depends(get_execution_service)
):
    success = await service.delete(execution_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Execution not found")
