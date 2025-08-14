from functools import lru_cache
from typing import Optional

from ..schemas.audit import AuditReport, AuditReportOptions
from ..client import N8nClient, get_n8n_client


class AuditService:
    def __init__(self, client: N8nClient):
        self.client = client

    async def generate_report(
        self, options: Optional[AuditReportOptions] = None
    ) -> AuditReport:
        payload = {}
        if options:
            payload = {"additionalOptions": options.model_dump(by_alias=True, exclude_none=True)}

        async with self.client.get_client() as http_client:
            response = await http_client.post("/audit", json=payload)
            response.raise_for_status()
            return AuditReport.model_validate(response.json())


@lru_cache
def get_audit_service(client: N8nClient = get_n8n_client()) -> AuditService:
    return AuditService(client)
