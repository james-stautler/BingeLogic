import styles from "styles/MetricsDisplay.module.css"

import Link from "next/link"
import SearchBar from "@/components/SearchBar"
import { useWindowSize } from "@/hooks/useWindowSize"

const POSTER_QUERY_URL = "https://image.tmdb.org/t/p/w780"
const BACKDROP_QUERY_URL = "https://image.tmdb.org/t/p/original"

interface MetricsModel {
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

interface EpisodeModel {
    id: number,
    season_number: number,
    episode_number: number,
    title: string,
    rating: number,
    air_date: string,
    vote_count: number
}

interface ShowModel {
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

function mapToShowModel(json: any): ShowModel {

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

function getPopularityTier(score: number): { label: string; color: string } {
    if (score >= 300) return { label: "High", color: "#FBBF24" }; // Emerald Green
    if (score >= 50) return { label: "Medium", color: "#34D399" }; // Your Azure Blue
    return { label: "Low", color: "#60A5FA" }; // Dimmed
}

export default async function Page({searchParams,}:{searchParams: Promise<{ [key: string]: string | string[] | undefined}>}) {

    const { query } = await searchParams;
    const response = await fetch(`https://bingelogic-backend.onrender.com/api/show_details?show_id=${query}`);

    const data = await response.json();
    const SHOW: ShowModel = mapToShowModel(data);
    const tier = getPopularityTier(SHOW.popularity);

    const POSTER_URL = POSTER_QUERY_URL + SHOW.poster_path;
    const BACKDROP_URL = BACKDROP_QUERY_URL + SHOW.backdrop_path;

    return (
        <div className={styles.MetricsDisplayContainer}>
            <SearchBar navBar={true} />
            <div className={styles.MetricsDisplayHero}>
                <div className={styles.MetricsDisplayHeroPoster}>
                    <img src={BACKDROP_URL}/>
                </div>
                <div className={styles.MetricsDisplayHeroMeta}>
                    <div className={styles.MetricsDisplayHeroMetaTitle}>
                        {SHOW.title}
                    </div>
                    <div className={styles.MetricsDisplayHeroMetaLogistics}>
                        {SHOW.first_air_date.slice(0,4) + " • "}
                        <span>{SHOW.number_of_seasons} {SHOW.number_of_seasons === 1 ? 'Season' : 'Seasons'}</span>
                        {" • " + SHOW.genres.join(" • ")}
                    </div>
                    <div className={styles.MetricsDisplayHeroMetaPopularity}>
                        {"TMDB Popularity: "}<span style={{color: tier.color}}>{tier.label}</span>
                    </div>
                    <div className={styles.MetricsDisplayHeroMetaOverview}>
                        {SHOW.overview}
                    </div>
                </div>
            </div>
        </div>
    )

};
