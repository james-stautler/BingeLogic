import pytest 
from services.tmdb_service import get_single_season

@pytest.mark.asyncio
async def test_imdb_get_single_season():

    show_id = 95396
    season = 2

    episodes = await get_single_season(show_id, season)
    
    print(episodes)

    assert len(episodes) > 0
    assert episodes[0].title == "Hello, Ms. Cobel"
