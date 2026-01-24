import pytest  
from services.tmdb_service import get_show_details

@pytest.mark.asyncio
async def test_imdb_service_get_details():

    show_id = "95396"

    res = await get_show_details(show_id)

    assert res["name"] == "Severance"
    assert res["id"] == 95396
