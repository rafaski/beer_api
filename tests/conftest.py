import pytest
from httpx import AsyncClient

from app.main import app


@pytest.fixture
async def client() -> AsyncClient:
    """
    Fixture to create an asynchronous HTTP client for testing FastAPI endpoints.
    """
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client
