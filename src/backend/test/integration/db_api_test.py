import asyncio
import pytest
from models.show_model import ShowModel, Episode, ShowMetrics
from crud.modeledQueries import insert_show, get_show_by_id, update_show, delete_show
from db.mongodb import client

@pytest.mark.asyncio
async def test_crud():

    test_id = 11
    await delete_show(test_id)

    show = ShowModel(
        id = test_id,
        title = "Test Show",
        overview = "Testing CRUD DB operations",
        number_of_seasons = 1,
        episodes = [
            Episode(season_number=1, episode_number=1, title="Pilot", rating=9.0)
        ],
        analysis=ShowMetrics(
            watchability_score = 90.0,
            rating_consistency = 1.0,
            momentum_score = 5.0,
            retention_rate = 100.0,
            consensus_gap = 0.0,
            popularity = 150.5
        )
    )

    await insert_show(show)
    fetched_show = await get_show_by_id(test_id)

    assert fetched_show is not None
    assert fetched_show.id == test_id
    assert fetched_show.title == "Test Show"
    assert len(fetched_show.episodes) == 1
    assert fetched_show.analysis.watchability_score == 90.0    
    assert fetched_show.last_updated is not None

    await  update_show(test_id, {"title": "New Title"})

    fetched_show = await get_show_by_id(test_id)
    assert fetched_show is not None
    assert fetched_show.title == "New Title"

    await delete_show(test_id)

    fetched_show = await get_show_by_id(test_id)

    assert fetched_show is None





    


