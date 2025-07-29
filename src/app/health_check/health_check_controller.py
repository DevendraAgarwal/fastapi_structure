"""API Controller for Health Check"""
from fastapi import APIRouter, status

from ...services.log_service import logger
from ...services.response_service import response

router = APIRouter(
    prefix="/app",
    tags=["HealthCheck"]
)


@router.get("/api/health-check", status_code=status.HTTP_200_OK)
async def health_check():
    """Main Health Check Function To Check All Services"""
    logger.debug({
        "event": "startup",
        "message": "Health Check Controller Called"
        })
    return response.add_message("Health Check OK").send_response()
