import abc

import asyncpg
import multiprocessing
import abc
from asyncpg import Pool


class AbstractDatabase(abc.ABC):
    @abc.abstractmethod
    async def _create_pool(self):
        pass

    @abc.abstractmethod
    async def get_pool(self):
        pass

    @abc.abstractmethod
    async def get_connection(self):
        pass

    @abc.abstractmethod
    async def _create_connection(self):
        pass


class AsyncDatabase(AbstractDatabase):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AsyncDatabase, cls).__new__(cls)
        return cls._instance

    def __init__(self,
                 user: str,
                 password: str,
                 host: str,
                 database_name: str,
                 min_size_pool: int = 1,
                 max_size_pool: int = multiprocessing.cpu_count()
                 ):
        self._user = user
        self._password = password
        self._host = host
        self._database_name = database_name
        self._min_size_pool = min_size_pool
        self._max_size_pool = max_size_pool
        self._pool = None
        self._conn = None

    async def get_pool(self) -> Pool:
        if self._pool is None:
            self._pool = await self._create_pool()
        return self._pool

    async def _create_pool(self) -> Pool:
        self._pool = await asyncpg.create_pool(user=self._user,
                                               password=self._password,
                                               database=self._database_name,
                                               host=self._host,
                                               min_size=self._min_size_pool,
                                               max_size=self._max_size_pool,
                                               )

        return self._pool

    async def get_connection(self):
        if self._conn is None:
            self._conn = await self._create_connection()
        return self._conn


    async def _create_connection(self):
        self.conn = await asyncpg.connect(user=self._user,
                                          password=self._password,
                                          database=self._database_name,
                                          host=self._host,
                                          )
        return self.conn





