import pytest


@pytest.mark.anyio
async def test_health_check(client):
    """
    Test health check endpoint.
    """

    response = await client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}
