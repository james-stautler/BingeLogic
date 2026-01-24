import httpx
import os
from dotenv import load_dotenv 
from models.show_model import ShowModel, Episode, ShowMetrics
from db.mongodb import client
from fastapi import HTTPException

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

async def get_show_details(show_id: str):

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
            return data
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="TMDB API Error")
        except Exception as e:
            raise HTTPException(status_code=500, details=f"Unexpected Error: {str(e)}")


    

