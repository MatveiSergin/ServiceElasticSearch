from parser import XmlParser
import asyncio
import time
from managers import XmlManager, ElasticSearchManager, ServiceManager


async def main():
    start = time.time()
    #await ServiceManager().process_offers()
    end = time.time()
    #print(end - start)
    start = end
    await ServiceManager().update_similar_sku_for_offers()
    end = time.time()
    print(end-start)
if __name__ == "__main__":
    asyncio.run(main())