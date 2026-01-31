from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

class SearchResult(BaseModel):
    tmdb_id: int
    title: str
    poster_path: Optional[str]
    release_date: Optional[str]

class Episode(BaseModel):
    id: int
    season_number: int
    episode_number: int
    title: str
    rating: float = Field(ge = 0, le = 10)
    air_date: Optional[str] = None
    vote_count: int = Field(default = 0)

class ShowMetrics(BaseModel):
    watchability_score: float = Field(ge = 0, le = 100)
    average_rating: float
    high_rating: float
    low_rating: float
    stinker_episodes: List[int]
    stinker_rating: float
    highlight_episodes: List[int]
    highlight_rating: float
    rating_consistency: float
    land_the_plane_score: float
    momentum_score: float
    retention_rate: float
    binge_index: float

class ShowModel(BaseModel):

    id: int = Field(alias="_id")
    title: str
    overview: Optional[str] = None
    poster_path: Optional[str] = None
    backdrop_path: Optional[str] = None
    first_air_date: Optional[str] = None
    genres: List[str] = []
    number_of_seasons: int
    popularity: float = Field(default=0.0)

    metrics: Optional[ShowMetrics] = None

    last_updated: datetime = Field(default_factory=datetime.now)

    episodes: List[Episode] = []

    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
        str_strip_whitespace=True
    )
