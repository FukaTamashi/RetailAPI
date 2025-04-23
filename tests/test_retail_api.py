import pytest
from fastapi.testclient import TestClient

from server.server import app
import api.retail_api.retail_api as retail_api_module
from api.retail_api.retail_api import get_crm_client


class DummyResponse:
    def __init__(self, status_code: int, body: any):
        self._status_code = status_code
        self._body = body

    def is_successful(self) -> bool:
        return True

    def get_status_code(self) -> int:
        return self._status_code

    def get_response(self) -> any:
        return self._body


class StubClient:
    async def get_customers(self, limit=20, page=1, filters=None):
        return DummyResponse(200, {
            "customers": [{"id": 1}],
            "pagination": {"limit": limit, "currentPage": page, "totalPageCount": 1, "totalCount": 1}
        })

    async def create_customer(self, customer: dict, site: str):
        return DummyResponse(200, {"id": 123})

    async def get_customer(self, customer_id: str | int, site: str, id_type: str = 'externalId'):
        return DummyResponse(200, {"customer": {"id": int(customer_id)}})

    async def get_orders(self, filters=None, limit=20, page=1):
        return DummyResponse(200, {
            "orders": [{"id": 1}],
            "pagination": {"limit": limit, "currentPage": page, "totalPageCount": 1, "totalCount": 1}
        })

    async def order_create(self, order: dict, site: str | None = None):
        return DummyResponse(200, {"id": 456})

    async def get_orders_by_customer(self, customer_id: int, site: str | None = None, limit: int = 20, page: int = 1):
        return DummyResponse(200, {
            "orders": [{"id": 1}],
            "pagination": {"limit": limit, "currentPage": page, "totalPageCount": 1, "totalCount": 1}
        })

    async def order_payment_create(self, payment: dict, site: str):
        return DummyResponse(200, {"id": 789})


@pytest.fixture(autouse=True)
def override_crm_client(monkeypatch):
    stub = StubClient()
    monkeypatch.setattr(retail_api_module, "get_crm_client", lambda: stub)


@pytest.fixture(scope="module")
def client():
    stub = StubClient()

    app.dependency_overrides[get_crm_client] = lambda: stub

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_list_customers(client):
    response = client.get("/api/retailCRM/customers")
    assert response.status_code == 200
    data = response.json()
    assert "customers" in data and isinstance(data["customers"], list)


def test_create_customer(client):
    payload = {"firstName": "John", "email": "john@example.com", "phone": "123", "countryIso": "RU"}
    response = client.post("/api/retailCRM/customers", json=payload)
    assert response.status_code == 200
    assert response.json() == {"id": 123}


def test_retrieve_customer(client):
    response = client.get("/api/retailCRM/customers/1")
    assert response.status_code == 200
    assert response.json() == {"customer": {"id": 1}}


def test_create_order(client):
    payload = {"customerId": 1, "externalId": "ORD-1", "items": [{"quantity": 2, "offerId": 10}]}
    response = client.post("/api/retailCRM/orders", json=payload)
    assert response.status_code == 200
    assert response.json() == {"id": 456}


def test_list_orders_by_customer(client):
    response = client.get("/api/retailCRM/orders/1")
    assert response.status_code == 200
    assert "orders" in response.json()


def test_create_payment(client):
    payload = {"payment": {"order": {"id": 1}, "amount": 100}, "site": "testfl"}
    response = client.post("/api/retailCRM/orders/payments", json=payload)
    assert response.status_code == 200
    assert response.json() == {"id": 789}
