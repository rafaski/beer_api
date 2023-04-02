from fastapi import FastAPI

from app.routers.fermentation import router

description = """
## Beer API ##
"""

app = FastAPI(
    title="Beer API",
    description=description
)

app.include_router(router=router)
