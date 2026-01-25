from fastapi import APIRouter, Query, BackgroundTasks
from datetime import datetime, timedelta, timezone
from services.tmdb_service import tmdb_get_show_details, tmdb_get_shows, tmdb_get_episodes_all_seasons
from crud.modeledQueries import db_get_show_by_id,db_insert_show
from core.metrics import getShowMetrics

shows_router = APIRouter()

@shows_router.get("/suggestions")
async def get_suggestions(query: str = Query(..., min_length=2)):

    res = await tmdb_get_shows(query)
    return res

async def full_refresh(show_id: int):

    show = await tmdb_get_show_details(show_id)
    episodes = await tmdb_get_episodes_all_seasons(show_id, show.number_of_seasons)
    metrics = getShowMetrics(episodes)
    
    show.episodes = episodes
    show.metrics = metrics
    show.last_updated = datetime.now(timezone.utc)
    
    id = await db_insert_show(show) 

    return show

@shows_router.get("/show_details")
async def get_show(show_id: int, backgroundTasks: BackgroundTasks):

    show = await db_get_show_by_id(show_id)
    if show:
        if (datetime.now(timezone.utc) - show.last_updated.replace(tzinfo=timezone.utc)) < timedelta(hours=24):
            return show
        
        backgroundTasks.add_task(full_refresh, show_id)
        return show
            
    show = await full_refresh(show_id)
    return show

    



    
        


