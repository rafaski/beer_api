from unittest.mock import patch

import pytest


@pytest.mark.asyncio
async def test_get_data_success(client):
    response = await client.get("/data")
    assert response.status_code == 200
    assert response.json() == {
        "message": (
            "Data successfully requested from Punk API and stored in database."
            " You can query data now."
        )
    }


@pytest.mark.asyncio
@patch("app.routers.data.punk_request")
async def test_get_data_json_structure_change(mock_punk_request, client):
    mock_punk_request.return_value = [{"id": 1, "name": "Test Beer"}]
    response = await client.get("/data")
    assert response.status_code == 500


@pytest.mark.asyncio
@patch("app.routers.data.punk_request")
async def test_get_data_error_handling(mock_punk_request, client):
    mock_punk_request.side_effect = Exception(
        "Simulated error in punk_request function"
    )
    response = await client.get("/data")
    assert response.status_code == 500
