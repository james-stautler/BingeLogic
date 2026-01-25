import asyncio
import pytest
from models.show_model import ShowModel, Episode, ShowMetrics
from crud.modeledQueries import db_insert_show, db_get_show_by_id, db_update_show, db_delete_show
from db.mongodb import client

@pytest.mark.asyncio
async def test_crud():

    test_id = 11
    await db_delete_show(test_id)

    show = ShowModel(
        id = test_id,
        title = "Test Show",
        overview = "Testing CRUD DB operations",
        number_of_seasons = 1,
        episodes = [
            Episode(id = 1024, season_number = 1, episode_number = 1, title = "Pilot", rating = 9.0)
        ],
        popularity = 28.4,
        metrics=ShowMetrics(
            watchability_score = 90.0,
            average_rating = 9.0,
            high_rating = 9.5,
            low_rating = 6.5,
            stinker_episodes = [1, 2, 3],
            stinker_rating = 3.2,
            highlight_episodes = [4, 5, 6],
            highlight_rating = 9.1,
            rating_consistency = 1.4,
            land_the_plane_score = 0.7,
            momentum_score = 1.3,
            retention_rate = 0.94,
            binge_index = 1.2
        )
    )

    await db_insert_show(show)
    fetched_show = await db_get_show_by_id(test_id)

    assert fetched_show is not None
    assert fetched_show.id == test_id
    assert fetched_show.title == "Test Show"
    assert len(fetched_show.episodes) == 1
    assert fetched_show.metrics.watchability_score == 90.0    
    assert fetched_show.last_updated is not None

    await  db_update_show(test_id, {"title": "New Title"})

    fetched_show = await db_get_show_by_id(test_id)
    assert fetched_show is not None
    assert fetched_show.title == "New Title"

    await db_delete_show(test_id)

    fetched_show = await db_get_show_by_id(test_id)

    assert fetched_show is None





    


