"""Custom Exception Class For Redis Service"""
from fastapi import HTTPException


class RedisNotInitializedException(HTTPException):
    """Error While Redis Service Not Initialized"""

    def __init__(self, error_message: str = ""):
        if error_message == "":
            error_message = "RedisService not initialized. Call `initialize()` first"
        super().__init__(status_code=404, detail=error_message)


class RedisAlreadyInitializedException(HTTPException):
    """Error While Redis Service Already Initialized"""

    def __init__(self, error_message: str = ""):
        if error_message == "":
            error_message = "RedisService is already initialized."
        super().__init__(status_code=404, detail=error_message)
