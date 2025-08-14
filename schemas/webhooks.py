from pydantic import BaseModel, Field
import uuid

class WebhookBase(BaseModel):
    name: str
    http_method: str
    path: str
    workflow_id: uuid.UUID

class WebhookCreate(WebhookBase):
    pass

class Webhook(WebhookBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)

    class Config:
        orm_mode = True
