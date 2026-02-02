"use client";

import { Line, LineChart, XAxis, YAxis, CartesianGrid, ReferenceLine } from "recharts";
import { ChartConfig, ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart";
import { Card, CardHeader, CardFooter, CardContent, CardTitle, CardDescription } from "./ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { ShowModel, EpisodeModel } from "@/components/showModel";
import { useState } from "react";

import styles from "styles/Graph.module.css"

export function getChartComponents(episodes: EpisodeModel[]) {
    
    const sortedEpisodes = [...episodes].sort((a, b) => 
        a.season_number - b.season_number || a.episode_number - b.episode_number
    );

    const continuousData = sortedEpisodes.map((ep, index) => ({
        absoluteEpisode: index + 1,
        episode: ep.episode_number,
        season: ep.season_number,
        rating: ep.rating,
        title: ep.title,
        [`Season ${ep.season_number}`]: ep.rating,
        all: ep.rating 
    }));

    const episodeRatingMap = new Map<number, Record<string, any>>();
    const seasonKeys = new Set<String>();

    for (let i = 0; i < episodes.length; i++) {
        
        if (!episodeRatingMap.has(episodes[i].episode_number)) {
            episodeRatingMap.set(episodes[i].episode_number, 
                                 { "episode" : episodes[i].episode_number,
                                    "title": episodes[i].title });
        }
        
        let seasonTag = "Season " + episodes[i].season_number.toString();
        const row = episodeRatingMap.get(episodes[i].episode_number);

        if (row) {
            row[seasonTag] = episodes[i].rating;
        }

        seasonKeys.add(seasonTag);
    }

    const overlapData = Array.from(episodeRatingMap.values()).sort((a, b) => a.episode - b.episode);

    return { continuousData, overlapData }; 

}

function getChartConfig(episodes: EpisodeModel[]): ChartConfig {

    const config: ChartConfig = {};
    const uniqueSeasons = Array.from(new Set(episodes.map(ep => ep.season_number))).sort((a, b) => a - b);

    uniqueSeasons.forEach((num) => {
        const key = `Season ${num}`;

        config[key] = {
            label: `Season ${num}`,
        };
    });

    return config;
}

export default function Graph({ show }: { show: ShowModel }) {

    const [ activeSeason, selectSeason ] = useState("all");

    const { continuousData, overlapData } = getChartComponents(show.episodes); 
    const chartConfig = getChartConfig(show.episodes);

    const currentData = activeSeason === "all" ? continuousData : overlapData;
    const xAxisKey = activeSeason === "all" ? "absoluteEpisode" : "episode";

    return (
        <div className={styles.GraphContainer}>
            <Card className={styles.CardContainer}> 
                <CardHeader className={styles.CardHeader}>
                    <CardDescription className={styles.CardDescription}>
                        Rating by Episode
                    </CardDescription>
                    <div className={styles.SelectContainer}>
                        <Select onValueChange={selectSeason} defaultValue="all">
                            <SelectTrigger className={styles.SelectTrigger}>
                                <SelectValue/>
                            </SelectTrigger>
                            <SelectContent position="popper" className={styles.SelectContent}>
                                <SelectItem value="all">Complete Series</SelectItem>
                                {Object.keys(chartConfig).map((key) => (
                                    <SelectItem className={styles.SelectItem} key={key} value={key}>
                                        {chartConfig[key].label}
                                    </SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                    </div>
                </CardHeader>

                <CardContent className={styles.CardContent}>
                    <ChartContainer className={styles.ChartContainer} config={chartConfig}>
                        <LineChart
                            className={styles.LineChart}
                            accessibilityLayer
                            data={currentData}
                            margin={{ bottom: 50, right: 20, top: 20}}
                        >
                            <CartesianGrid vertical={false} />
 
                            <XAxis
                                dataKey={xAxisKey}
                                tickLine={false}
                                axisLine={false}
                                tickMargin={25}
                                padding={{ left:20 }}
                                tick={{ fill: '#71717a', fontSize: 12 }}
                                label={{ 
                                    value: activeSeason === "all" ? "Absolute Episode #" : "Episode #", 
                                    position: 'insideBottom', 
                                    offset: -30 
                                }} 
                            />
                      
                            <YAxis
                                domain={[0, 10]}
                                width={40} 
                                tickLine={false}
                                axisLine={false}
                                tick={{ fill: '#71717a', fontSize: 12 }}
                                ticks={[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
                                interval={0}
                                label={{
                                    value: "Rating",
                                    angle: -90,
                                    position: "insideLeft",
                                    style: { textAnchor: 'middle' }
                                }}
                            />
                            
                            <ChartTooltip
                                cursor={false}
                                content={({ active, payload }) => {
                                    if (active && payload && payload.length) {

                                        const data = payload[0].payload;
                                        const epDisplay = activeSeason === "all" ? data.absoluteEpisode : data.episode;
                                        const ratingDisplay = activeSeason === "all" ? data.rating : data[activeSeason];

                                        return (
                                            <div className="border border-[var(--border)] px-2 py-2 rounded">
                                                <div className="text-[var(--foreground)]">
                                                    {"Episode " + epDisplay} 
                                                </div>
                                                <div className="text-[var(--foreground)] italic">
                                                    {"\"" + data.title + "\""} 
                                                </div>
                                                <div className="text-[var(--foreground)]">
                                                    {"Rating: " + ratingDisplay}
                                                </div>
                                            </div>
                                        ); 
                                    }
                                    return null;
                                }}
                            />

                           {activeSeason === "all" ? (
                                <Line 
                                    dataKey="all" 
                                    type="linear" 
                                    strokeWidth={2} 
                                    dot={false} 
                                />
                            ) : (
                                <Line 
                                    dataKey={activeSeason} 
                                    type="linear" 
                                    strokeWidth={4} 
                                    dot={ true } 
                                />
                            )}

                            <ReferenceLine
                                y={show.metrics.average_rating}
                                stroke="var(--muted-foreground)"
                            />
                            
                            <ReferenceLine
                                    y={show.metrics.stinker_rating}
                                    stroke="var(--red)"
                            />

                            <ReferenceLine
                                y={show.metrics.highlight_rating}
                                stroke="var(--magenta)"
                            />
                        </LineChart>
                    </ChartContainer>
                </CardContent>
            </Card>
        </div>
    )
};
