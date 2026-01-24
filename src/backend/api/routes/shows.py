from fastapi import APIRouter, Query
from services.tmdb_service import get_show_details, get_shows

shows_router = APIRouter()

@shows_router.get("/suggestions")
async def get_suggestions(query: str = Query(..., min_length=2)):

    res = await get_shows(query)
    return res

#@shows_router.get("/show_details")
#async def get_suggestions(show_id: int):
    
    # This function should do the following:
    # Check the DB for cached show information + metrics (and validity) -> return if present
    # Fetch show details and episodes
    # Calculate metrics and store everything together in single model
    # Async write to DB, return model to webpage
