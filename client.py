import httpx
from functools import lru_cache

from app.core.config import settings


class N8nClient:
    """
    An HTTP client for interacting with the n8n API, handling authentication.
    """

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def get_client(self) -> httpx.AsyncClient:
        """
        Returns an authenticated httpx.AsyncClient.
        """
        return httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Accept": "application/json",
                "X-N8N-API-KEY": self.api_key,
            },
        )


@lru_cache
def get_n8n_client() -> N8nClient:
    """
    Dependency to get a singleton instance of the N8nClient.
    """
    return N8nClient(
        base_url=str(settings.n8n.N8N_BASE_URL),
        api_key=settings.n8n.N8N_API_KEY,
    )
