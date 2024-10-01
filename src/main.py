import asyncio
import time
from managers import ServiceManager


async def main():
    start = time.time()
    await ServiceManager().process_offers()
    end = time.time()
    print("time process offers:", end - start)
    start = end
    await ServiceManager().update_similar_sku_for_offers()
    end = time.time()
    print("time updating process", end - start)


if __name__ == "__main__":
    asyncio.run(main())
