"""Custom Middleware For Serve Application"""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class AppMiddleware(BaseHTTPMiddleware):
    """Application Middleware for All Request

    Args:
        BaseHTTPMiddleware (_type_): _description_
    """

    async def dispatch(self, request: Request, call_next):
        # Perform operations before the request is processed
        response = await call_next(request)
        # Perform operations after the request is processed
        return response
