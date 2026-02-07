import styles from "styles/MetricsDisplay.module.css"

import SearchBar from "@/components/SearchBar"
import { Card, CardHeader, CardDescription, CardTitle } from "@/components/ui/card"
import mapToShowModel, { ShowModel } from "@/components/showModel"
import Graph from "../../components/Graph"
import Link from "next/link"

const POSTER_QUERY_URL = "https://image.tmdb.org/t/p/w780"
const BACKDROP_QUERY_URL = "https://image.tmdb.org/t/p/original"

function getPopularityTier(score: number): { label: string; color: string } {
    if (score >= 300) return { label: "High", color: "#FBBF24" }; // Emerald Green
    if (score >= 50) return { label: "Medium", color: "#34D399" }; // Your Azure Blue
    return { label: "Low", color: "#60A5FA" }; // Dimmed
}

type MetricType = 'binge' | 'watchability' | 'momentum' | 'consistency' | 'rating' | 'land_the_plane' | 'retention';

export function getMetricColor(value: number, type: MetricType): string {

    const thresholds: Record<MetricType, { gold: number; green: number; orange: number }> = {
        binge: { gold: 85, green: 60, orange: 35 },
        watchability: { gold: 90, green: 70, orange: 40 },
        momentum: { gold: 66, green: 55, orange: 45 },
        consistency: { gold: 93, green: 80, orange: 60 },
        rating: { gold: 9.0, green: 7.5, orange: 5.5 },
        land_the_plane: { gold: 90, green: 75, orange: 60},
        retention: { gold: 75, green: 55, orange: 40 },
    };

    const t = thresholds[type];

    if (value >= t.gold) return 'var(--magenta)';   
    if (value >= t.green) return 'var(--green)';  
    if (value >= t.orange) return 'var(--orange)';
    return 'var(--red)';                        
}

export default async function Page({searchParams,}:{searchParams: Promise<{ [key: string]: string | string[] | undefined}>}) {

    const { query } = await searchParams;
    const response = await fetch(`https://bingelogic-backend.onrender.com/api/show_details?show_id=${query}`);

    const data = await response.json();
    const SHOW: ShowModel = mapToShowModel(data);
    const tier = getPopularityTier(SHOW.popularity);

    const stinkerPercentage = 100 * (SHOW.metrics.stinker_episodes.length / SHOW.episodes.length);
    const highlightPercentage = 100 * (SHOW.metrics.highlight_episodes.length / SHOW.episodes.length);

    const BACKDROP_URL = BACKDROP_QUERY_URL + SHOW.backdrop_path;
    
    const averageColor = getMetricColor(SHOW.metrics.average_rating, "rating");
    const highColor = getMetricColor(SHOW.metrics.high_rating, "rating");
    const lowColor = getMetricColor(SHOW.metrics.low_rating, "rating");
    const stinkerColor = getMetricColor(SHOW.metrics.stinker_rating, "rating");
    const highlightColor = getMetricColor(SHOW.metrics.highlight_rating, "rating");
    const watchabilityColor = getMetricColor(SHOW.metrics.watchability_score, "watchability");
    const bingeColor = getMetricColor(SHOW.metrics.binge_index, "binge");
    const ratingConsistencyColor = getMetricColor(SHOW.metrics.rating_consistency, "consistency");
    const landThePlaneColor = getMetricColor(SHOW.metrics.land_the_plane_score, "land_the_plane");
    const momentumColor = getMetricColor(SHOW.metrics.momentum_score, "momentum");
    const retentionColor = getMetricColor(SHOW.metrics.retention_rate, "retention");

    return (
        <div className={styles.MetricsPageContainer}>
            <div className={styles.MetricsDisplayContainer}>
                <div className={styles.MetricsDisplayNav}>
                    <Link href="/" className={styles.MetricsDisplayNavHome}>
                        [BINGE LOGIC]
                    </Link>
                    <SearchBar navBar={true} />
                </div>
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
                <div className={styles.MetricsDisplayHelpLink}>
                    What do these metrics mean?
                </div>
                <div className={styles.MetricsDisplayHeroCardGridContainer}>
                    <Card className={styles.MetricsDisplayCardContainer}>
                        <CardHeader className={styles.MetricsDisplayCardHeader}>
                            <CardDescription className={styles.MetricsDisplayCardDescription}>
                                Watchability Score
                            </CardDescription>
                            <CardTitle className={styles.MetricsDisplayCardTitle} style={{color: watchabilityColor}}>
                                {SHOW.metrics.watchability_score}
                            </CardTitle>
                        </CardHeader>
                    </Card>
                    <Card className={styles.MetricsDisplayCardContainer}>
                        <CardHeader className={styles.MetricsDisplayCardHeader}>
                            <CardDescription className={styles.MetricsDisplayCardDescription}>
                                Binge Index
                            </CardDescription>
                            <CardTitle className={styles.MetricsDisplayCardTitle} style={{color: bingeColor }}>
                                {SHOW.metrics.binge_index}
                            </CardTitle>
                        </CardHeader>
                    </Card>
                    <Card className={styles.MetricsDisplayCardContainer}>
                        <CardHeader className={styles.MetricsDisplayCardHeader}>
                            <CardDescription className={styles.MetricsDisplayCardDescription}>
                                Rating Consistency
                            </CardDescription>
                            <CardTitle className={styles.MetricsDisplayCardTitle} style={{color: ratingConsistencyColor}}>
                                {SHOW.metrics.rating_consistency}
                            </CardTitle>
                        </CardHeader>
                    </Card>
                    <Card className={styles.MetricsDisplayCardContainer}>
                        <CardHeader className={styles.MetricsDisplayCardHeader}>
                            <CardDescription className={styles.MetricsDisplayCardDescription}>
                                Land the Plane Score
                            </CardDescription>
                            <CardTitle className={styles.MetricsDisplayCardTitle} style={{color: landThePlaneColor}}>
                                {SHOW.metrics.land_the_plane_score}
                            </CardTitle>
                        </CardHeader>
                    </Card>
                    <Card className={styles.MetricsDisplayCardContainer}>
                        <CardHeader className={styles.MetricsDisplayCardHeader}>
                            <CardDescription className={styles.MetricsDisplayCardDescription}>
                                Momentum Score
                            </CardDescription>
                            <CardTitle className={styles.MetricsDisplayCardTitle} style={{color: momentumColor}}>
                                {SHOW.metrics.momentum_score}
                            </CardTitle>
                        </CardHeader>
                    </Card>
                    <Card className={styles.MetricsDisplayCardContainer}>
                        <CardHeader className={styles.MetricsDisplayCardHeader}>
                            <CardDescription className={styles.MetricsDisplayCardDescription}>
                                Retention Rate
                            </CardDescription>
                            <CardTitle className={styles.MetricsDisplayCardTitle} style={{color: retentionColor}}>
                                {SHOW.metrics.retention_rate}
                            </CardTitle>
                        </CardHeader>
                    </Card>
                </div>
                <div className={styles.MetricsDisplayGranularDataContainer}> 
                    <Graph show={SHOW}/>
                    <div className={styles.MetricsDisplayGranularCardContainer}>
                        <div className={styles.MetricsDisplayRatingCardContainer}>
                            <Card className={styles.MetricsDisplayCardContainer}>
                                <CardHeader className={styles.MetricsDisplayCardHeader}>
                                    <CardDescription className={styles.MetricsDisplayCardDescription}>
                                        Average Rating
        </CardDescription>
                                    <CardTitle className={styles.MetricsDisplayCardTitle} style={{color: averageColor}}>
                                        {SHOW.metrics.average_rating}
                                    </CardTitle>
                                </CardHeader>
                            </Card>
                            <Card className={styles.MetricsDisplayCardContainer}>
                                <CardHeader className={styles.MetricsDisplayCardHeader}>
                                    <CardDescription className={styles.MetricsDisplayCardDescription}>
                                        High Rating
                                    </CardDescription>
                                    <CardTitle className={styles.MetricsDisplayCardTitle} style={{color: highColor}}>
                                        {SHOW.metrics.high_rating}
                                    </CardTitle>
                                </CardHeader>
                            </Card>
                            <Card className={styles.MetricsDisplayCardContainer}>
                                <CardHeader className={styles.MetricsDisplayCardHeader}>
                                    <CardDescription className={styles.MetricsDisplayCardDescription}>
                                        Low Rating
                                    </CardDescription>
                                    <CardTitle className={styles.MetricsDisplayCardTitle} style={{color: lowColor}}>
                                        {SHOW.metrics.low_rating}
                                    </CardTitle>
                                </CardHeader>
                            </Card>
                        </div>
                        <div className={styles.MetricsDisplayLongRatingCardContainer}>
                            <Card className={styles.MetricsDisplayCardContainer}>
                                <CardHeader className={styles.MetricsDisplayCardHeader}>
                                    <CardDescription className={styles.MetricsDisplayCardDescription}>
                                        Average Highlight Rating
                                    </CardDescription>
                                    <CardTitle className={styles.MetricsDisplayCardTitle} style={{color: highlightColor}}>
                                        {SHOW.metrics.highlight_rating}
                                    </CardTitle>
                                </CardHeader>
                            </Card>
                            <Card className={styles.MetricsDisplayCardContainer}>
                                <CardHeader className={styles.MetricsDisplayCardHeader}>
                                    <CardDescription className={styles.MetricsDisplayCardDescription}>
                                        Highlight Episode Count
                                    </CardDescription>
                                    <CardTitle className={styles.MetricsDisplayCardTitle} style={{color: highlightColor}}>
                                        {SHOW.metrics.highlight_episodes.length} <span className="text-sm">{" (" + highlightPercentage.toFixed(2) + "%)"}</span>

                                    </CardTitle>
                                </CardHeader>
                            </Card>
                            <Card className={styles.MetricsDisplayCardContainer}>
                                <CardHeader className={styles.MetricsDisplayCardHeader}>
                                    <CardDescription className={styles.MetricsDisplayCardDescription}>
                                        Average Stinker Rating
                                    </CardDescription>
                                    <CardTitle className={styles.MetricsDisplayCardTitle} style={{color: stinkerColor}}>
                                        {SHOW.metrics.stinker_rating}
                                    </CardTitle>
                                </CardHeader>
                            </Card>
                            <Card className={styles.MetricsDisplayCardContainer}>
                                <CardHeader className={styles.MetricsDisplayCardHeader}>
                                    <CardDescription className={styles.MetricsDisplayCardDescription}>
                                        Stinker Episode Count
                                    </CardDescription>
                                    <CardTitle className={styles.MetricsDisplayCardTitle} style={{color: stinkerColor}}>
                                        {SHOW.metrics.stinker_episodes.length} <span className="text-sm">{" (" + stinkerPercentage.toFixed(2) + "%)"}</span>
                                    </CardTitle>
                                </CardHeader>
                            </Card>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )

};
