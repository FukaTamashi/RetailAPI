from typing import Optional, Dict, Any, List

from fastapi import APIRouter, Query, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from api.base_api.api_client_retailcrm import ApiClientRetailCRM
from config import settings

retail_router = APIRouter()


def get_crm_client() -> ApiClientRetailCRM:
    return ApiClientRetailCRM(
        crm_base_url=settings.base_url,
        crm_api_key=settings.api_key,
    )


class FilterParams(BaseModel):
    name: Optional[str]
    email: Optional[str]
    createdAtFrom: Optional[str]
    createdAtTo: Optional[str]


class OrderItem(BaseModel):
    quantity: int
    offerId: Optional[int] = None
    offerExternalId: Optional[str] = None
    offerXmlId: Optional[str] = None


class CreateOrderRequest(BaseModel):
    customerId: Optional[int] = Field(None, description="Internal ID of the customer")
    customerExternalId: Optional[str] = Field(None, description="External ID of the customer")
    customerBrowserId: Optional[str] = Field(None, description="Browser ID in Collector")

    externalId: Optional[str] = Field(None, description="External order number (order number)")
    items: List[OrderItem]

    site: Optional[str] = None


class CreateCustomerRequest(BaseModel):
    firstName: str = Field(..., description="Имя клиента")
    lastName: Optional[str] = Field(None, description="Фамилия клиента")
    email: str = Field(..., description="Email клиента")
    phone: str = Field(..., description="Телефон клиента")
    countryIso: str = Field(..., description="ISO code of client's country, e.g. RU")
    site: Optional[str] = Field(None, description="Shop code, defaults to configured site_code")


class CreatePaymentRequest(BaseModel):
    payment: Dict[str, Any]
    site: str


@retail_router.get("/customers", summary="Get list of customers with filters")
async def list_customers(
        name: Optional[str] = Query(None),
        email: Optional[str] = Query(None),
        createdAtFrom: Optional[str] = Query(None),
        createdAtTo: Optional[str] = Query(None),
        limit: int = Query(20, ge=1),
        page: int = Query(1, ge=1),
        client: ApiClientRetailCRM = Depends(get_crm_client)
):
    filters: Dict[str, Any] = {}
    if name:
        filters['name'] = name
    if email:
        filters['email'] = email
    if createdAtFrom:
        filters['dateFrom'] = createdAtFrom
    if createdAtTo:
        filters['dateTo'] = createdAtTo

    resp = await client.get_customers(limit=limit, page=page, filters=filters)
    if not resp.is_successful():
        raise HTTPException(status_code=resp.get_status_code(), detail=resp.get_response())
    return resp.get_response()


@retail_router.post("/customers", summary="Create a new customer")
async def create_customer(
        body: CreateCustomerRequest,
        client: ApiClientRetailCRM = Depends(get_crm_client)
):
    cust_data = body.model_dump(exclude={"site"}, exclude_none=True)
    site_code = body.site or settings.site_code
    resp = await client.create_customer(customer=cust_data, site=site_code)
    if not resp.is_successful():
        raise HTTPException(status_code=resp.get_status_code(), detail=resp.get_response())
    return resp.get_response()


@retail_router.get("/customers/{customer_id}", summary="Get a customer by ID")
async def retrieve_customer(
        customer_id: str,
        by: str = Query('id', alias='by'),
        site: Optional[str] = Query(None),
        client: ApiClientRetailCRM = Depends(get_crm_client)
):
    site_code = site or settings.site_code
    resp = await client.get_customer(customer_id=customer_id, site=site_code, id_type=by)
    if not resp.is_successful():
        raise HTTPException(status_code=resp.get_status_code(), detail=resp.get_response())
    return resp.get_response()


@retail_router.post("/orders", summary="Create a new order with customer, items and externalId")
async def create_order(
    body: CreateOrderRequest,
    client: ApiClientRetailCRM = Depends(get_crm_client)
):
    order_payload: Dict[str, Any] = {}

    if body.customerId is not None:
        order_payload["customer"] = {"id": body.customerId}
    elif body.customerExternalId:
        order_payload["customer"] = {"externalId": body.customerExternalId}
    elif body.customerBrowserId:
        order_payload["customer"] = {"browserId": body.customerBrowserId}

    order_payload["externalId"] = body.externalId

    order_payload["items"] = []
    for item in body.items:
        item_payload = {"quantity": item.quantity}
        offer = {}
        if item.offerId:
            offer["id"] = item.offerId
        if item.offerExternalId:
            offer["externalId"] = item.offerExternalId
        if item.offerXmlId:
            offer["xmlId"] = item.offerXmlId
        if offer:
            item_payload["offer"] = offer
        order_payload["items"].append(item_payload)

    site_code = body.site or settings.site_code
    resp = await client.order_create(order=order_payload, site=site_code)
    if not resp.is_successful():
        raise HTTPException(status_code=resp.get_status_code(), detail=resp.get_response())
    return resp.get_response()


@retail_router.get("/orders/{customer_id}", summary="Get order by customer ID")
async def get_order(
    customer_id: int,
    by: str = Query('id', alias='by'),
    site: Optional[str] = Query(None),
    client: ApiClientRetailCRM = Depends(get_crm_client)
):
    site_code = site or settings.site_code
    resp = await client.get_orders_by_customer(customer_id=customer_id, site=site_code)
    if not resp.is_successful():
        raise HTTPException(status_code=resp.get_status_code(), detail=resp.get_response())
    return resp.get_response()


@retail_router.post("/orders/payments", summary="Create and attach payment to order")
async def create_payment(
        body: CreatePaymentRequest,
        client: ApiClientRetailCRM = Depends(get_crm_client)
):
    resp = await client.order_payment_create(payment=body.payment, site=body.site)
    if not resp.is_successful():
        raise HTTPException(status_code=resp.get_status_code(), detail=resp.get_response())
    return resp.get_response()
