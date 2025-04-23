from typing import List
import json
from api.base_api.client_base import BaseClient
import logging


class ApiClientRetailCRM(BaseClient):

    def __init__(self, crm_base_url, crm_api_key):
        BaseClient.__init__(self, crm_base_url=crm_base_url, crm_api_key=crm_api_key)
        self.logger = logging.getLogger(__name__)

    async def get_customers(self,
                            limit: int = 100,
                            page: int = 1,
                            filters: dict = None):
        """
        :param limit: integer
        :param page: integer
        :param filters: dict
        :return: Response
        """
        try:
            params = {
                'limit': limit,
                'page': page,
            }

            if filters:
                for k, v in filters.items():
                    params[f"filter[{k}]"] = v

            return await self.get(
                endpoint=f"/customers",
                params=params
            )

        except Exception as e:
            self.logger.error(e)

    async def create_customer(self,
                              customer: dict,
                              site: str):
        """
        :param customer: dict
        :param site: string
        :return: Response
        """
        try:

            data = {
                'site': site,
                'customer': json.dumps(
                    customer
                ),
            }

            return await self.post(
                endpoint='/customers/create',
                json=data
            )

        except Exception as e:
            self.logger.error(e)

    async def get_customer(self,
                           customer_id: str | int,
                           site: str,
                           id_type: str = 'externalId'):
        """
        :param customer_id: string or integer
        :param site: string
        :param id_type: string
        :return: Response
        """
        try:
            params = {
                'site': site,
                'by': id_type
            }

            return await self.get(
                endpoint=f'/customers/{customer_id}',
                params=params
            )

        except Exception as e:
            self.logger.error(e)

    async def order_create(self, order: dict, site: str | None = None):
        """
        :param order: dict — заказ (ключи customer, items, externalId и т.д.)
        :param site: str | None — код магазина
        :return: Response
        """
        try:
            data = {
                'order': json.dumps(order)
            }

            if site is not None:
                data['site'] = site

            return await self.post(
                endpoint='/orders/create',
                json=data
            )
        except Exception as e:
            self.logger.error(f"Ошибка при создании заказа: {e}")
            raise

    async def get_orders_by_customer(
            self,
            customer_id: int,
            site: str | None = None,
            limit: int = 20,
            page: int = 1
    ):

        try:
            params = {
                'limit': limit,
                'page': page,
                'filter[customerId]': customer_id,
            }
            if site:
                params['site'] = site

            return await self.get(
                endpoint='/orders',
                params=params
            )
        except Exception as e:
            self.logger.error(f"Error fetching orders by customer: {e}")
            raise

    async def order_payment_create(self,
                                   payment: dict,
                                   site: str):
        """
        :param payment: dict
        :param site: string
        :return: Response
        """
        try:
            data = {
                'site': site,
                'payment': json.dumps(
                    payment
                ),
            }

            return await self.post(
                endpoint='/orders/payments/create',
                json=data
            )
        except Exception as e:
            self.logger.error(e)
