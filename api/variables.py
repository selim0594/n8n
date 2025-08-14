from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from ..schemas.variables import Variable, VariableCreate, VariableUpdate
from ..services.variables import VariableService, get_variable_service

router = APIRouter()


@router.get("/", response_model=List[Variable])
async def list_variables(service: VariableService = Depends(get_variable_service)):
    return await service.get_all()


@router.post("/", response_model=Variable, status_code=status.HTTP_201_CREATED)
async def create_variable(variable_in: VariableCreate, service: VariableService = Depends(get_variable_service)):
    return await service.create(variable_in)


@router.get("/{variable_id}", response_model=Variable)
async def get_variable(variable_id: str, service: VariableService = Depends(get_variable_service)):
    variable = await service.get_by_id(variable_id)
    if not variable:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Variable not found")
    return variable


@router.put("/{variable_id}", response_model=Variable)
async def update_variable(
    variable_id: str, variable_in: VariableUpdate, service: VariableService = Depends(get_variable_service)
):
    variable = await service.update(variable_id, variable_in)
    if not variable:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Variable not found")
    return variable


@router.delete("/{variable_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_variable(variable_id: str, service: VariableService = Depends(get_variable_service)):
    success = await service.delete(variable_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Variable not found")
