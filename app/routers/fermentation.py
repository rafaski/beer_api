from fastapi import APIRouter

router = APIRouter(tags=["fermentation"])


@router.get("/currencies")
async def currencies() -> str:
    """
    Get a list of all supported currencies
    """
    return "example"
