from fastapi import FastAPI

from app.routers.fermentation import router
from app.dependencies.punk_client import punk_request

description = """
## Beer API ##
"""

app = FastAPI(
    title="Beer API",
    description=description
)


@app.on_event("startup")
def get_data() -> None:
    """Get all data"""
    punk_request()


app.include_router(router=router)

