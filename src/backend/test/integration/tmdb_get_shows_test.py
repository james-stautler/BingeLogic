import pytest
from services.tmdb_service import tmdb_get_shows

@pytest.mark.asyncio
async def test_imdb_service_get_shows():
    query = "severance"

    results = await tmdb_get_shows(query)

    assert isinstance(results, list)
    assert len(results) > 0

    first_result = results[0]
    assert first_result.title == "Severance"
    assert first_result.release_date == "2022-02-17"
