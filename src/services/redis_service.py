"""Redis Service"""
from typing import Optional
from threading import Lock

import redis

from src.exceptions.redis_exceptions import (
    RedisAlreadyInitializedException,
    RedisNotInitializedException
)


class RedisService:
    """Redis Class Service

    Raises:
        RedisNotInitializedException: _description_
        RedisAlreadyInitializedException: _description_

    Returns:
        _type_: _description_
    """
    _instance = None
    _lock = Lock()
    _client: Optional[redis.Redis] = None

    def __init__(
        self,
        host: str,
        port: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        db: int = 0
    ):
        if RedisService._client is not None:
            raise RedisAlreadyInitializedException()

        RedisService._client = redis.Redis(
            host=host,
            port=port,
            username=username,
            password=password,
            db=db,
            decode_responses=True  # by that you get str, not bytes
        )

    @classmethod
    def initialize(
        cls,
        host: str,
        port: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        db: int = 0
    ) -> 'RedisService':
        """_summary_

        Args:
            host (str): _description_
            port (int): _description_
            username (Optional[str], optional): _description_. Defaults to None.
            password (Optional[str], optional): _description_. Defaults to None.
            db (int, optional): _description_. Defaults to 0.

        Returns:
            RedisService: _description_
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls(host, port, username, password, db)
        return cls._instance

    @classmethod
    def get_instance(cls) -> 'RedisService':
        """_summary_

        Raises:
            Exception: _description_

        Returns:
            RedisService: _description_
        """
        if cls._instance is None:
            raise RedisNotInitializedException()
        return cls._instance

    def set(self, key: str, value: str, ex: Optional[int] = None) -> None:
        """_summary_

        Args:
            key (str): _description_
            value (str): _description_
            ex (Optional[int], optional): _description_. Defaults to None.
        """
        RedisService._client.set(name=key, value=value, ex=ex)

    def get(self, key: str) -> Optional[str]:
        """_summary_

        Args:
            key (str): _description_

        Returns:
            Optional[str]: _description_
        """
        return RedisService._client.get(name=key)

    def close(self):
        """_summary_
        """
        if RedisService._client:
            RedisService._client.close()
