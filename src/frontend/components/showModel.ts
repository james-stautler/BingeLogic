export interface MetricsModel {
    watchability_score: number,
    average_rating: number,
    high_rating: number,
    low_rating: number,
    stinker_episodes: number[],
    stinker_rating: number,
    highlight_episodes: number[],
    highlight_rating: number,
    rating_consistency: number,
    land_the_plane_score: number, 
    momentum_score: number,
    retention_rate: number, 
    binge_index: number,
}

export interface EpisodeModel {
    id: number,
    season_number: number,
    episode_number: number,
    title: string,
    rating: number,
    air_date: string,
    vote_count: number
}

export interface ShowModel {
    id: number,
    title: string,
    overview: string,
    poster_path: string,
    backdrop_path: string,
    first_air_date: string,
    genres: string[],
    number_of_seasons: number,
    popularity: number,
    metrics: MetricsModel,
    last_updated: string,
    episodes: EpisodeModel[]
}

export default function mapToShowModel(json: any): ShowModel {

  return {
    id: json.id,
    title: json.title ?? "Unknown Title",
    overview: json.overview ?? "",
    poster_path: json.poster_path ?? "",
    backdrop_path: json.backdrop_path ?? "",
    first_air_date: json.first_air_date ?? "",
    genres: Array.isArray(json.genres) ? json.genres : [],
    number_of_seasons: json.number_of_seasons ?? 0,
    popularity: json.popularity ?? 0,
    last_updated: json.last_updated ?? new Date().toISOString(),
    
    metrics: {
      watchability_score: json.metrics?.watchability_score ?? 0,
      average_rating: json.metrics?.average_rating ?? 0,
      high_rating: json.metrics?.high_rating ?? 0,
      low_rating: json.metrics?.low_rating ?? 0,
      stinker_episodes: json.metrics?.stinker_episodes ?? [],
      stinker_rating: json.metrics?.stinker_rating ?? 0,
      highlight_episodes: json.metrics?.highlight_episodes ?? [],
      highlight_rating: json.metrics?.highlight_rating ?? 0,
      rating_consistency: json.metrics?.rating_consistency ?? 0,
      land_the_plane_score: json.metrics?.land_the_plane_score ?? 0,
      momentum_score: json.metrics?.momentum_score ?? 0,
      retention_rate: json.metrics?.retention_rate ?? 0,
      binge_index: json.metrics?.binge_index ?? 0,
    },

    episodes: Array.isArray(json.episodes) 
      ? json.episodes.map((ep: any): EpisodeModel => ({
          id: ep.id,
          season_number: ep.season_number,
          episode_number: ep.episode_number,
          title: ep.title ?? "Untitled Episode",
          rating: ep.rating ?? 0,
          air_date: ep.air_date ?? "",
          vote_count: ep.vote_count ?? 0,
        }))
      : [],
  };

}

