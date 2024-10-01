import uuid
from repository import IRepository, OfferRepository


class OfferService:
    def __init__(self, repository: IRepository = OfferRepository):
        self.repository = repository()

    async def create_offer(self, offer: dict) -> dict:
        return await self.repository.create(offer)

    async def delete_offer(self, offer_id: int) -> None:
        pass

    async def get_offer(self, offer_id: int) -> dict:
        pass

    async def fetch_uuids(self, chunk_size=1000):
        async for uuids in self.repository.read_uuids(chunk_size):
            yield uuids

    async def update_similar_sku_offer(self, values: list[tuple[str, list[uuid.UUID]]]) -> None:
        await self.repository.update_similar_sku_offer(values)
