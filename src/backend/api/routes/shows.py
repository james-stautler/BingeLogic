import os
from fastapi import APIRouter, Query, BackgroundTasks, Header, HTTPException
from datetime import datetime, timedelta, timezone
from services.tmdb_service import tmdb_get_show_details, tmdb_get_shows, tmdb_get_episodes_all_seasons
from crud.modeledQueries import db_get_show_by_id,db_insert_show, db_delete_show, db_delete_many_shows, db_get_cursor
from core.metrics import getShowMetrics
from db.mongodb import db, DatabaseCollections

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

async def cleanup():
    
    projection = {"id": 1, "last_updated": 1}
    cursor = db_get_cursor(projection) 

    ids_to_delete = []

    async for show in cursor:
        if (datetime.now(timezone.utc) - show["last_updated"].replace(tzinfo=timezone.utc)) > timedelta(days=30):
            ids_to_delete.append(show["id"])

    if ids_to_delete:
        await db_delete_many_shows(ids_to_delete) 
    
@shows_router.post("/cleanup")
async def trigger_cleanup(backgroundTasks: BackgroundTasks, token: str = Header(None)):
    
    print(os.getenv("CLEANUP_TOKEN"))
    if token != os.getenv("CLEANUP_TOKEN"):
        raise HTTPException(status_code=403)

    backgroundTasks.add_task(cleanup)

    return {
        "status": "accepted",
        "message": "Cleanup task backgrounded successfully.",
        "timestamp_utc": datetime.now(timezone.utc).isoformat()
    }


    
    



    
        


