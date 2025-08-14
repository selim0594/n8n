from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from ..schemas.credentials import Credential, CredentialCreate, CredentialUpdate
from ..services.credentials import CredentialService, get_credential_service

router = APIRouter()


@router.get("/", response_model=List[Credential])
async def list_credentials(service: CredentialService = Depends(get_credential_service)):
    return await service.get_all()


@router.post("/", response_model=Credential, status_code=status.HTTP_201_CREATED)
async def create_credential(
    credential_in: CredentialCreate, service: CredentialService = Depends(get_credential_service)
):
    return await service.create(credential_in)


@router.get("/{credential_id}", response_model=Credential)
async def get_credential(
    credential_id: str, service: CredentialService = Depends(get_credential_service)
):
    credential = await service.get_by_id(credential_id)
    if not credential:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Credential not found")
    return credential


@router.patch("/{credential_id}", response_model=Credential)
async def update_credential(
    credential_id: str,
    credential_in: CredentialUpdate,
    service: CredentialService = Depends(get_credential_service),
):
    credential = await service.update(credential_id, credential_in)
    if not credential:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Credential not found")
    return credential


@router.delete("/{credential_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_credential(
    credential_id: str, service: CredentialService = Depends(get_credential_service)
):
    success = await service.delete(credential_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Credential not found")
