import pytest
from services.tmdb_service import tmdb_get_episodes_all_seasons

@pytest.mark.asyncio
async def test_tmdb_get_all_seasons():
    
    show_id = 95396
    seasons = 2

    episodes = await tmdb_get_episodes_all_seasons(show_id, seasons)

    assert episodes is not None
    assert len(episodes) > 0

    

    

