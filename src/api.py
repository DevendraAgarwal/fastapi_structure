""" Combine All API Routes Here
"""
from fastapi import FastAPI

# Import all Controller Routes Here
from src.app.health_check.health_check_controller import (
    router as health_check_router
)

# Register Routers


def register_routes(app: FastAPI):
    """Define All Controller Routes in This Function

    Args:
        app (FastAPI): App Object To Include Routes
    """
    app.include_router(health_check_router, include_in_schema=True)
