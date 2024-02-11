import pytest


@pytest.mark.asyncio
async def test_get_avg_fermentation_temp_by_hop_all_success(client):
    response = await client.get("/avg_fermentation_temp_by_hop")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_avg_fermentation_temp_primary_hops_success(client):
    response = await client.get("/avg_fermentation_temp_primary_hops")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_10_most_used_hops_success(client):
    response = await client.get("/most_used_hops")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_beers_by_temp_success(client):
    response = await client.get("/beers_by_temp?temp=20")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_hops_by_amount_success(client):
    response = await client.get("/hops_by_amount?amount=50")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_beers_by_hop_success(client):
    response = await client.get("/beers_by_hop?hop_name=test_hop")
    assert response.status_code == 200
