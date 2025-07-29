"""Custom Exception Class For GCP Secret Manager"""
from fastapi import HTTPException


class SecretManagerException(HTTPException):
    """Error While Issue in Fetching Secret Manager Data"""

    def __init__(self, secret_key: str):
        error_message = f"Error While Fetching Secret Key Value {secret_key}"
        super().__init__(status_code=404, detail=error_message)
