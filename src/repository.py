import asyncio
import uuid
from abc import ABC, abstractmethod

import asyncpg

from database import AbstractDatabase, AsyncDatabase
from settings import settings
from sql_query import INSERT_OFFER, OFFER_UPDATE, GET_COUNT_OFFERS, SELECT_UUID_FROM_OFFERS


class IRepository(ABC):
    @abstractmethod
    async def create(self, item: dict) -> dict:
        pass

    @abstractmethod
    async def read(self, item_id: str) -> dict:
        pass

    @abstractmethod
    async def update(self, product: dict) -> None:
        pass

    @abstractmethod
    async def delete(self, item_id: str) -> None:
        pass


class OfferRepository(IRepository):

    def __init__(self,
                 db: AbstractDatabase = AsyncDatabase
                 ):
        self.inst_db = db(user=settings.DB_USER,
                          password=settings.DB_PASSWORD,
                          host=settings.DB_HOST,
                          database_name=settings.DB_NAME,
                          )

    async def create(self, offer: dict) -> dict:
        pool = await self.inst_db.get_pool()
        async with pool.acquire() as conn:
            await conn.execute(INSERT_OFFER,
                                 offer['uuid'],
                                 offer['marketplace_id'],
                                 offer['product_id'],
                                 offer['title'],
                                 offer['description'],
                                 offer['brand'],
                                 offer['seller_id'],
                                 offer['seller_name'],
                                 offer['first_image_url'],
                                 offer['category_id'],
                                 offer['category_lvl_1'],
                                 offer['category_lvl_2'],
                                 offer['category_lvl_3'],
                                 offer['category_remaining'],
                                 offer['features'],
                                 offer['rating_count'],
                                 offer['rating_value'],
                                 offer['price_before_discounts'],
                                 offer['discount'],
                                 offer['price_after_discounts'],
                                 offer['bonuses'],
                                 offer['sales'],
                                 offer['inserted_at'],
                                 offer['updated_at'],
                                 offer['currency'],
                                 offer['barcode'],
                                 )

    async def read(self, offer_id: str) -> dict:
        pass

    async def update_similar_sku_offer(self, values: list[str, list[uuid.UUID]]) -> None:
        pool = await self.inst_db.get_pool()
        async with pool.acquire() as conn:
            tasks = []
            for value, offer_id in values:
                tasks.append(conn.execute(OFFER_UPDATE, value, offer_id))

            await asyncio.gather(*tasks)

    async def read_uuids(self, limit: int) -> list[str]:
        pool = await self.inst_db.get_pool()
        total = await self.get_count()
        async with pool.acquire() as conn:
            for offset in range(0, total, limit):
                response = await conn.fetch(
                    SELECT_UUID_FROM_OFFERS,
                    offset,
                    limit
                )
                uuids = []
                for record in response:
                    uuids.append(record['uuid'])
                yield uuids

    async def get_count(self):
        conn = await self.inst_db.get_connection()
        total_records = await conn.fetchval(GET_COUNT_OFFERS)
        return total_records

    async def update(self, offer: dict) -> None:
        pass

    async def delete(self, offer_id: str) -> None:
        pass
