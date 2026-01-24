from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

class Episode(BaseModel):
    season_number: int
    episode_number: int
    title: str
    rating: float = Field(ge = 0, le = 10)
    air_date: Optional[str] = None
    vote_count: int = Field(default = 0)

class ShowMetrics(BaseModel):
    watchability_score: float = Field(ge = 0, le = 100)
    rating_consistency: float
    momentum_score: float
    retention_rate: float
    consensus_gap: float
    popularity: float = Field(default=0.0)

class ShowModel(BaseModel):

    id: int = Field(alias="_id")
    title: str
    overview: Optional[str] = None
    poster_path: Optional[str] = None
    first_air_date: Optional[str] = None
    genres: List[str] = []
    number_of_seasons: int

    last_updated: datetime = Field(default_factory=datetime.now)

    episodes: List[Episode] = []

    analysis: Optional[ShowMetrics] = None

    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
        str_strip_whitespace=True
    )
