from typing import List, Dict
import uuid
from ..schemas.webhooks import Webhook, WebhookCreate

class WebhookService:
    def __init__(self):
        self.webhooks: Dict[uuid.UUID, Webhook] = {}

    def get_all(self) -> List[Webhook]:
        return list(self.webhooks.values())

    def get_by_id(self, webhook_id: uuid.UUID) -> Webhook | None:
        return self.webhooks.get(webhook_id)

    def create(self, webhook_create: WebhookCreate) -> Webhook:
        new_webhook = Webhook(**webhook_create.dict())
        self.webhooks[new_webhook.id] = new_webhook
        return new_webhook

    def delete(self, webhook_id: uuid.UUID) -> Webhook | None:
        return self.webhooks.pop(webhook_id, None)

webhook_service = WebhookService()
