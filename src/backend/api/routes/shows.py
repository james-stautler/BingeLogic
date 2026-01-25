from fastapi import APIRouter, Query
from datetime import datetime, timedelta, timezone
from services.tmdb_service import tmdb_get_show_details, tmdb_get_shows, tmdb_get_episodes_all_seasons
from crud.modeledQueries import db_get_show_by_id
from core.metrics import getShowMetrics

shows_router = APIRouter()

@shows_router.get("/suggestions")
async def get_suggestions(query: str = Query(..., min_length=2)):

    res = await tmdb_get_shows(query)
    return res

@shows_router.get("/show_details")
async def get_show(show_id: int):
    
    # This function should do the following:
    # Check the DB for cached show information + metrics (and validity) -> return if present
    # Fetch show details and episodes
    # Calculate metrics and store everything together in single model
    # Async write to DB, return model to webpage

    show = await db_get_show_by_id(show_id)
    if show:
        if (datetime.now(timezone.utc) - show.last_updated) > timedelta(hours=24):
            return show

    show = await tmdb_get_show_details(show_id)
    episodes = await tmdb_get_episodes_all_seasons(show_id, show.number_of_seasons)
    metrics = getShowMetrics(episodes)
    
    show.episodes = episodes
    show.metrics = metrics

    return show

    



    
        


