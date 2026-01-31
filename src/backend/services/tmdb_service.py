import httpx
import os
import asyncio

from models.show_model import SearchResult, ShowModel, Episode, ShowMetrics
from fastapi import HTTPException
from typing import List

TMDB_READ_TOKEN = os.getenv("TMDB_READ_TOKEN")

async def tmdb_get_shows(query: str, client: httpx.AsyncClient = None) -> List[SearchResult]:
    
    url = "https://api.themoviedb.org/3/search/tv"
    headers = {
        "Authorization": f"Bearer {TMDB_READ_TOKEN}",
        "accept": "application/json"
    }
    
    try:
        res = None
        if client:
            res = await client.get(url, headers=headers, params={"query": query})
        else:
            async with httpx.AsyncClient() as c:
                res = await c.get(url, headers=headers, params={"query":query})

        res.raise_for_status()

        data = res.json()
        results = data.get("results", [])
        return [
                SearchResult(
                    tmdb_id=show["id"],
                    title=show["name"],
                    poster_path=show.get("poster_path"),
                    release_date=show.get("first_air_date")
                )
                for show in results
        ]      
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="TMDB API Error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected Error: {str(e)}")

async def tmdb_get_show_details(show_id: int, client: httpx.AsyncClient = None) -> ShowModel:

    url = f"https://api.themoviedb.org/3/tv/{show_id}"
    headers = {
        "Authorization": f"Bearer {TMDB_READ_TOKEN}",
        "accept": "application/json"
    }

    try:
        res = None
        if client:
            res = await client.get(url, headers=headers)
        else:
            async with httpx.AsyncClient() as c:
                res = await c.get(url, headers=headers)

        res.raise_for_status()
        data = res.json()

        return ShowModel(
            id = data["id"],
            title = data["name"],
            overview = data["overview"],
            poster_path = data["poster_path"],
            backdrop_path = data["backdrop_path"],
            first_air_date = data["first_air_date"],
            genres = [item["name"] for item in data["genres"]],
            number_of_seasons = data["number_of_seasons"],
            popularity = round(data["popularity"], 2)
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="TMDB API Error")
    except Exception as e:
        raise HTTPException(status_code=500, details=f"Unexpected Error: {str(e)}")

async def tmdb_get_episodes_single_season(show_id: int, season: int, client: httpx.AsyncClient = None) -> List[Episode]:

    url = f"https://api.themoviedb.org/3/tv/{show_id}/season/{season}"
    headers = {
        "Authorization": f"Bearer {TMDB_READ_TOKEN}",
        "accept": "application/json"
    }

    try:
        res = None
        if client:
            res = await client.get(url, headers=headers)
        else:
            async with httpx.AsyncClient() as c:
                res = await c.get(url, headers=headers)
        
        res.raise_for_status()
        data = res.json()

        Episodes = [
            Episode(
                id=item["id"],
                season_number=season,
                episode_number=item["episode_number"],
                title=item["name"],
                rating=item["vote_average"],
                air_date=item.get("air_date"),
                vote_count=item["vote_count"]
            )
            for item in data.get("episodes", [])
        ]

        return [e for e in Episodes if e.rating > 0 and e.vote_count > 0] 

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="TMDB API Error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected Error: {str(e)}")
        

async def tmdb_get_episodes_all_seasons(show_id: int, number_of_seasons: int) -> List[Episode]:

    async with httpx.AsyncClient() as client:

        tasks = [
            tmdb_get_episodes_single_season(show_id, i, client)
            for i in range(1, number_of_seasons + 1)
        ]

        all_seasons = await asyncio.gather(*tasks)


        return [episode for season in all_seasons for episode in season]

