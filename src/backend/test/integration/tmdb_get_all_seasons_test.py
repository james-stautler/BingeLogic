import pytest
from services.tmdb_service import get_all_seasons

@pytest.mark.asyncio
async def test_tmdb_get_all_seasons():
    
    show_id = 95396
    seasons = 2

    seasons = await get_all_seasons(show_id, seasons)

    assert seasons is not None
    assert len(seasons) == 2

    

    

