import pytest
from services.tmdb_service import get_shows

@pytest.mark.asyncio
async def test_imdb_service_get_shows():
    query = "severance"

    results = await get_shows(query)

    assert isinstance(results, list)
    assert len(results) > 0

    first_result = results[0]
    assert "tmdb_id" in first_result
    assert "title" in first_result
    assert "Severance" in first_result["title"]
