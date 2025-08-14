from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from ..schemas.tags import Tag, TagCreate, TagUpdate
from ..services.tags import TagService, get_tag_service

router = APIRouter()


@router.get("/", response_model=List[Tag])
async def list_tags(service: TagService = Depends(get_tag_service)):
    # Note: The n8n API for listing tags returns a dict with a 'data' key.
    # The service handles this, so the router just returns the result.
    return await service.get_all()


@router.post("/", response_model=Tag, status_code=status.HTTP_201_CREATED)
async def create_tag(tag_in: TagCreate, service: TagService = Depends(get_tag_service)):
    return await service.create(tag_in)


@router.get("/{tag_id}", response_model=Tag)
async def get_tag(tag_id: str, service: TagService = Depends(get_tag_service)):
    tag = await service.get_by_id(tag_id)
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag


@router.put("/{tag_id}", response_model=Tag)
async def update_tag(
    tag_id: str, tag_in: TagUpdate, service: TagService = Depends(get_tag_service)
):
    tag = await service.update(tag_id, tag_in)
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(tag_id: str, service: TagService = Depends(get_tag_service)):
    success = await service.delete(tag_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
