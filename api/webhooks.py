from fastapi import APIRouter, HTTPException, status
from typing import List
import uuid
from ..schemas.webhooks import Webhook, WebhookCreate
from ..services.webhooks import webhook_service

router = APIRouter()

@router.get("/", response_model=List[Webhook])
def list_webhooks():
    return webhook_service.get_all()

@router.post("/", response_model=Webhook, status_code=status.HTTP_201_CREATED)
def create_webhook(webhook_in: WebhookCreate):
    return webhook_service.create(webhook_in)

@router.get("/{webhook_id}", response_model=Webhook)
def get_webhook(webhook_id: uuid.UUID):
    webhook = webhook_service.get_by_id(webhook_id)
    if not webhook:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Webhook not found")
    return webhook

@router.delete("/{webhook_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_webhook(webhook_id: uuid.UUID):
    webhook = webhook_service.delete(webhook_id)
    if not webhook:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Webhook not found")
