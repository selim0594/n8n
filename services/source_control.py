from functools import lru_cache
from typing import Optional

from ..schemas.source_control import SourceControlPullResult, SourceControlPullOptions
from ..client import N8nClient, get_n8n_client


class SourceControlService:
    def __init__(self, client: N8nClient):
        self.client = client

    async def pull(
        self, options: Optional[SourceControlPullOptions] = None
    ) -> SourceControlPullResult:
        payload = {}
        if options:
            payload = options.model_dump(by_alias=True, exclude_none=True)

        async with self.client.get_client() as http_client:
            response = await http_client.post("/source-control/pull", json=payload)
            response.raise_for_status()
            return SourceControlPullResult.model_validate(response.json())


@lru_cache
def get_source_control_service(client: N8nClient = get_n8n_client()) -> SourceControlService:
    return SourceControlService(client)
