"""
Redis Async Singleton Service
This module provides an async singleton service for managing Redis connections
using a connection pool. It supports async context management and is designed
to handle high concurrency scenarios efficiently.
"""
import threading
import functools
from typing import Any, Dict, List, Callable, Optional, Awaitable, Union

# Ensure you have redis-py installed for async support
# pip install redis-py>=5.0.0
import redis.asyncio as redis

from src.meta_classes.async_singleton_meta import AsyncSingletonMeta


class AsyncRedisService(metaclass=AsyncSingletonMeta):
    """
    Async Redis Singleton supporting async context manager and connection pooling.
    """
    _instance = None
    _new_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        """
        Ensures only one instance is created (Singleton pattern).
        Thread-safe for concurrent environments.
        """
        if cls._instance is None:
            with cls._new_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self._pool: Optional[redis.ConnectionPool] = None
        self._client: Optional[redis.Redis] = None
        self._lock = threading.RLock()

    async def set_connection_pool(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: str = None,
        max_connections: int = 100,
        **kwargs
    ):
        """
        Setup the async Redis connection pool.
        """
        with self._lock:
            self._pool = redis.ConnectionPool(
                host=host,
                port=port,
                db=db,
                password=password,
                max_connections=max_connections,
                decode_responses=True,
                **kwargs,
            )
            self._client = redis.Redis(connection_pool=self._pool)

    def get_connection(self) -> redis.Redis:
        """
        Return the Redis client (async).
        """
        if self._client is None:
            raise Exception("Connection pool not set. Call set_connection_pool() first.")
        return self._client

    async def aclose(self):
        """
        Close the Redis connection pool and client.
        """
        with self._lock:
            if self._client:
                await self._client.aclose()
            if self._pool:
                await self._pool.aclose()
            self._client = None
            self._pool = None

    async def __aenter__(self):
        # Use with 'async with' for resource management
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.aclose()

    async def get(self, key: str) -> Any:
        """
        Get value by key, async.
        """
        client = self.get_connection()
        return await client.get(key)

    async def set(self, key: str, value: Any, expire: int = None) -> bool:
        """
        Set value (optionally with expiry in seconds), async.
        """
        client = self.get_connection()
        return await client.set(key, value, ex=expire)

    async def mget(self, keys: List[str]) -> List[Any]:
        """
        Get multiple values, async.
        """
        client = self.get_connection()
        return await client.mget(keys)

    async def mset(self, mapping: Dict[str, Any]) -> bool:
        """
        Set multiple key-value pairs, async.
        """
        client = self.get_connection()
        return await client.mset(mapping)

    async def get_by_pattern(self, pattern: str) -> Dict[str, Any]:
        """
        Get all key-value pairs matching a pattern, async.
        """
        client = self.get_connection()
        keys = await client.keys(pattern)
        if not keys:
            return {}
        values = await client.mget(keys)
        return {k: v for k, v in zip(keys, values)}

    async def delete(self, key: str) -> int:
        """
        Delete key, async.
        """
        client = self.get_connection()
        return await client.delete(key)

    async def exists(self, key: str) -> bool:
        """
        Check if key exists, async.
        """
        client = self.get_connection()
        return (await client.exists(key)) == 1

    def set_decorator(self, key: Union[str, Callable], expire: int = None) -> Callable:
        """
        Decorator for caching function result under a given key, async.
        Usage: @redis_instance.set_decorator("mykey")
        """
        def decorator(func: Callable[..., Awaitable]):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                result = await func(*args, **kwargs)
                await self.set(key, result, expire=expire)
                return result
            return wrapper
        return decorator if callable(key) is False else decorator(key)

    async def keys(self, pattern: str = "*") -> List[str]:
        """
        List all keys matching a pattern, async.
        """
        client = self.get_connection()
        return await client.keys(pattern)

    async def flushdb(self):
        """
        Delete all keys in the current database (DANGEROUS!), async.
        """
        client = self.get_connection()
        await client.flushdb()

    async def pipeline(self):
        """
        Get an async pipeline for batch commands (advanced usage).
        """
        client = self.get_connection()
        return client.pipeline()

# Usage Example for 100+ concurrency
import asyncio

async def main():
    redis_singleton = AsyncRedisService()
    await redis_singleton.set_connection_pool(
        host="localhost", port=6379, db=0, max_connections=200  # supports >100 concurrency
    )

    # Set and get single entry
    await redis_singleton.set("foo", "bar")
    value = await redis_singleton.get("foo")
    print(value)  # 'bar'

    # MSET & MGET
    await redis_singleton.mset({"a": "one", "b": "two"})
    values = await redis_singleton.mget(["a", "b"])
    print(values)  # ['one', 'two']

    # Pattern match
    await redis_singleton.set("data:model:1:2", "hello")
    print(await redis_singleton.get_by_pattern("data:model:1:*"))  # {'data:model:1:2': 'hello'}

    # Demonstrate 100+ concurrent writes
    tasks = [
        redis_singleton.set(f"user:{i}", f"id_{i}") for i in range(120)
    ]
    await asyncio.gather(*tasks)

    # Use as an async context manager (pool closes on exit)
    async with AsyncRedisService() as cm:
        await cm.set("bar", "baz")
        assert await cm.get("bar") == "baz"

    await redis_singleton.aclose()

async def pipeline_demo():
    redis_singleton = AsyncRedisService()
    await redis_singleton.set_connection_pool(host="localhost", port=6379, db=0)

    # Get a pipeline from the singleton
    pipe = await redis_singleton.pipeline()
    
    # Queue commands (these do NOT run until you execute())
    pipe.set("pkey1", "value1")
    pipe.set("pkey2", "value2")
    pipe.incr("pkey3")
    pipe.mget("pkey1", "pkey2")
    
    # Send all commands at once and get results
    results = await pipe.execute()
    print(results)  # [True, True, value_of_pkey3_after_incr, ['value1', 'value2']]

    await redis_singleton.aclose()

# Note: The above code is designed to be run in an async environment.
# If you're using this in a script, ensure to run it within an event loop.

# If you're using this in a script, you can run the main function like this:
# asyncio.run(main())

# Uncomment the following lines to run the main example
# asyncio.run(main())

# Uncomment the following lines to run the pipeline example
# asyncio.run(pipeline_demo())
