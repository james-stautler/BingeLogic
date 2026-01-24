import httpx
import os
import asyncio
from models.show_model import ShowModel, Episode, ShowMetrics
from fastapi import HTTPException
from typing import List

TMDB_READ_TOKEN = os.getenv("TMDB_READ_TOKEN")

async def get_shows(query: str):
    
    url = "https://api.themoviedb.org/3/search/tv"
    headers = {
        "Authorization": f"Bearer {TMDB_READ_TOKEN}",
        "accept": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(url, headers=headers, params={"query": query})
            res.raise_for_status()

            data = res.json()
            results = data.get("results", [])
            return [
                    {
                        "tmdb_id": show["id"],
                        "title": show["name"],
                        "overview": show.get("overview"),
                        "poster_path": show.get("poster_path"),
                        "release_date": show.get("first_air_date")
                    }
                    for show in results
            ]
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="TMDB API Error")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected Error: {str(e)}")

async def get_show_details(show_id: int) -> ShowModel:

    url = f"https://api.themoviedb.org/3/tv/{show_id}"
    headers = {
        "Authorization": f"Bearer {TMDB_READ_TOKEN}",
        "accept": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(url, headers=headers)
            res.raise_for_status()
            data = res.json()

            return ShowModel(
                id = data["id"],
                title = data["name"],
                overview = data["overview"],
                poster_path = data["poster_path"],
                first_air_date = data["first_air_date"],
                genres = [item["name"] for item in data["genres"]],
                number_of_seasons = data["number_of_seasons"]
            )
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="TMDB API Error")
        except Exception as e:
            raise HTTPException(status_code=500, details=f"Unexpected Error: {str(e)}")

async def get_single_season(show_id: int, season: int, client: httpx.AsyncClient = None) -> List[Episode]:

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

        return [
            Episode(
                season_number=season,
                episode_number=item["episode_number"],
                title=item["name"],
                rating=item["vote_average"],
                air_date=item.get("air_date"),
                vote_count=item["vote_count"]
            )
            for item in data.get("episodes", [])
        ]

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="TMDB API Error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected Error: {str(e)}")
        

async def get_all_seasons(show_id: int, number_of_seasons: int) -> List[List[Episode]]:

    async with httpx.AsyncClient() as client:

        tasks = [
            get_single_season(show_id, i, client)
            for i in range(1, number_of_seasons + 1)
        ]

        all_seasons = await asyncio.gather(*tasks)
        return all_seasons

