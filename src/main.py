""" Main Entry File Of Application
"""
from fastapi import FastAPI

from src.middlewares.app_middleware import AppMiddleware

from .api import register_routes

app = FastAPI()

# Adding Application Middleware
app.add_middleware(AppMiddleware)

# Registering All Routes Which Include in api.py
register_routes(app)
