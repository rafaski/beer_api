from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(tags=["health"])


@router.get("/ping")
async def health_check() -> JSONResponse:
    """
    Health check endpoint.
    Returns 200 if the service is up and running.
    """
    return JSONResponse(content={"message": "pong"})
