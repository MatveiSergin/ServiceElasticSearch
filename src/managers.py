import asyncio
from datetime import datetime
from elasticsearch.helpers import async_bulk
from parser import XmlParserProtocol, XmlParser
from service import OfferService
from utils import get_category_lvls, calculate_discount, conversion_from_str_to_int_or_none
import uuid
import multiprocessing
import elasticsearch as es
from settings import settings


class XmlManager:
    def __init__(self,
                 xml_parser: XmlParserProtocol = XmlParser,
                 offer_service: OfferService = OfferService,
                 ):
        self.xml_path = settings.XML_FILE_PATH
        self.inst_xml_parser = xml_parser(self.xml_path)
        self.inst_offer_service = offer_service()

    def get_categories(self) -> dict:
        categories = {}
        categories_generator = self.inst_xml_parser.parse_xml(tag="category")
        for category_data in categories_generator:
            cat_id, cat_parent = category_data.get("id"), category_data.get("parentId", None)
            categories[cat_id] = {
                "id": category_data.get("id"),
                "name": category_data.get("category"),
                "parent_id": category_data.get("parentId", None)
            }
        return categories

    async def get_offers(self) -> dict:
        categories = self.get_categories()
        offers_generator = self.inst_xml_parser.parse_xml(tag="offer")
        for offer in offers_generator:
            cat_id = offer.get("categoryId", None)

            if cat_id is not None:
                lvl_1, lvl_2, lvl_3, lvls_remaining = get_category_lvls(categories, cat_id)
            else:
                lvl_1 = lvl_2 = lvl_3 = lvls_remaining = None

            old_price = offer.get("oldprice", None)
            price = offer.get("price", None)

            if old_price is not None and price is not None:
                old_price = int(old_price)
                price = int(price)
                discount = calculate_discount(old_price, price)
            else:
                old_price = price = discount = None

            time = conversion_from_str_to_int_or_none(offer.get("modified_time", None))

            if time is not None:
                time = datetime.fromtimestamp(time)

            barcode = conversion_from_str_to_int_or_none(offer.get("barcode", None))
            category_id = conversion_from_str_to_int_or_none(offer.get("categoryId", None))
            product_id = conversion_from_str_to_int_or_none(offer.get("id", None))

            offer_data = {
                "uuid": uuid.uuid4(),
                "marketplace_id": 1,
                "product_id": product_id,
                "title": offer.get("name", None),
                "description": offer.get("description", None),
                "brand": offer.get("vendor", None),
                "seller_id": None,
                "seller_name": offer.get("vendor", None),
                "first_image_url": offer.get("picture", None),
                "category_id": category_id,
                "category_lvl_1": lvl_1,
                "category_lvl_2": lvl_2,
                "category_lvl_3": lvl_3,
                "category_remaining": lvls_remaining,
                "features": None,
                "rating_count": None,
                "rating_value": None,
                "price_before_discounts": old_price,
                "discount": discount,
                "price_after_discounts": price,
                "bonuses": None,
                "sales": None,
                "inserted_at": time,
                "updated_at": time,
                "currency": offer.get("currencyId", None),
                "barcode": barcode,
            }

            yield offer_data


class ElasticSearchManager:
    def __init__(self):
        self._elastic_search = es.AsyncElasticsearch(hosts=[settings.ELASTICSEARCH_URL])

    async def insert_offers(self, offers: list[dict]) -> None:
        docs = []

        for offer in offers:
            docs.append(
                {
                    "_op_type": "index",
                    "_index": "sku",
                    "_id": str(offer['uuid']),
                    "_source": {"title": offer["title"], "description": offer["description"], "brand": offer["brand"]}
                }
            )

        await async_bulk(self._elastic_search, docs)

    async def find_similar_sku(self, offer_uuid: str) -> list[uuid.UUID]:
        body = {
            "query": {
                "more_like_this": {
                    "fields": ["title", "description", "brand"],
                    "like": [{"_id": offer_uuid}],
                    "min_term_freq": 1,
                    "max_query_terms": 10
                }
            }
        }
        response = await self._elastic_search.search(index="sku", body=body)
        similar_uuids = [uuid.UUID(hit["_id"]) for hit in response["hits"]["hits"][:5]]
        return similar_uuids

    async def close_conn(self):
        await self._elastic_search.close()


class ServiceManager:
    def __init__(self,
                 xml_parser: XmlParserProtocol = XmlParser,
                 offer_service: OfferService = OfferService,
                 xml_manager: XmlManager = XmlManager,
                 elastic_search_manager: ElasticSearchManager = ElasticSearchManager
                 ):
        self._xml_manager = xml_manager(xml_parser, offer_service)
        self._elastic_search_manager = elastic_search_manager()
        self.ints_offer_service = offer_service()

    async def process_offers(self) -> None:
        offers = []
        offers_for_es = []

        async for offer in self._xml_manager.get_offers():

            offers.append(offer)

            if len(offers) > multiprocessing.cpu_count():
                tasks = [self._xml_manager.inst_offer_service.create_offer(offer) for offer in offers]
                offers_for_es.extend(offers)

                if len(offers_for_es) > multiprocessing.cpu_count() * 100:
                    await asyncio.gather(*tasks, self._elastic_search_manager.insert_offers(offers_for_es))
                    offers_for_es = []
                else:
                    await asyncio.gather(*tasks)
                offers = []

        if len(offers) > 0:
            tasks = [self._xml_manager.inst_offer_service.create_offer(offer) for offer in offers]
            await asyncio.gather(*tasks)
        if len(offers_for_es) > 0:
            await self._elastic_search_manager.insert_offers(offers_for_es)

        await self._elastic_search_manager.close_conn()

    async def update_similar_sku_for_offers(self):
        tasks = []
        values = []
        async for uuids in self.ints_offer_service.fetch_uuids():
            for offer_id in uuids:
                tasks += [self._elastic_search_manager.find_similar_sku(offer_id)]
            res = await asyncio.gather(*tasks)
            tasks = []
            values += [value for value in zip(uuids, res)]
            await self.ints_offer_service.update_similar_sku_offer(values)
