import httpx

from api.base_api.response import Response


class BaseClient:
    """
    Client base class of RetailCRM
    """

    def __init__(self, crm_base_url, crm_api_key):
        self.crm_base_url = crm_base_url
        self.crm_api_key = crm_api_key

        if self.crm_api_key:
            self.headers = {
                'X-API-KEY': self.crm_api_key
            }
        else:
            raise ValueError("ApiKey is None")

        if self.crm_base_url:
            self.client = httpx.AsyncClient(base_url=str(self.crm_base_url) + '/api/v5')
        else:
            raise ValueError("ApiUrl is None")

    async def close_client(self):
        if self.client:
            await self.client.aclose()

    async def post(self, endpoint, params=None, json=None, timeout=None) -> Response:
        try:
            response = await self.client.post(
                endpoint,
                params=params,
                json=json,
                timeout=timeout,
                headers=self.headers
            )
            return Response.from_httpx(response)
        except httpx.HTTPError as e:
            print(f"[POST ERROR] {e}")
            raise

    async def get(self, endpoint, params=None, timeout=None) -> Response:
        try:
            response = await self.client.get(
                endpoint,
                params=params,
                timeout=timeout,
                headers=self.headers
            )
            return Response.from_httpx(response)
        except httpx.HTTPError as e:
            print(f"[GET ERROR] {e}")
            raise
