import statistics
import numpy as np
from models.show_model import ShowMetrics, Episode
from typing import List

MIN_HIGHLIGHT_SCORE = 8.5
MAX_STINKER_SCORE = 6.0

def getStinkerScore(ratings: List[float]) -> float:

    stdev = statistics.stdev(ratings) if len(ratings) > 1 else 0
    avg = statistics.median(ratings)

    return round(max(MAX_STINKER_SCORE, avg - (2 * stdev)), 2)

def getHighlightScore(ratings: List[float]) -> float:
    
    stdev = statistics.stdev(ratings) if len(ratings) > 1 else 0
    avg = statistics.median(ratings)

    return round(min(MIN_HIGHLIGHT_SCORE, avg + (2 * stdev)), 2)

def getLandThePlaneScore(ratings: List[float]) -> float:

    if len(ratings) < 5: 
        return round(sum(ratings)/len(ratings) * 10, 2)

    episodeCount = max(2, int(len(ratings) * 0.1))
    
    seriesAvg = statistics.mean(ratings)
    landingAvg = statistics.mean(ratings[-episodeCount:])
    
    base = seriesAvg * 10
    delta = landingAvg - seriesAvg
    modifier = 0

    if delta < 0:
        if abs(delta) < 0.5:
            modifier = delta * 10
        else:
            modifier = delta * 30
        
        if landingAvg < 6.5:
            modifier -= 20
    else:
        modifier = min(10, delta * 10)

    score = base + modifier

    return round(max(0.0, min(100.0, score)), 2)

def getMomentum(ratings: List[float]) -> float:
    
    if len(ratings) < 5:
        return 0.0

    x = np.arange(len(ratings))
    y = np.array(ratings)

    slope, _ = np.polyfit(x, y, 1)
    
    scale_factor = 100 + (len(ratings) * 5)
    score = 50 + (slope * scale_factor)
    return round(max(0, min(100, score)), 2)


def getRatingConsistency(ratings: List[float]) -> float:
    
    if len(ratings) < 2:
        return 100.0

    stdev = statistics.stdev(ratings)
    score = 100 * (1 - (stdev / 2.0))

    return round(max(0.0, min(100.0, score)), 2)

def getRetentionRate(voteCounts: List[int]) -> float:
    
    if voteCounts[0] == 0:
        return 0.0
    
    retention_ratio = voteCounts[-1] / voteCounts[0]
    return round(min(retention_ratio * 100, 100.0), 2)

def getBingeIndex(episodes: List[Episode]) -> float:
    
    if len(episodes) < 3:
        return 50.0

    series_avg_rating = statistics.mean([episode.rating for episode in episodes])
    series_avg_vote_count = statistics.mean([episode.vote_count for episode in episodes])

    season_map = {}
    for episode in episodes:
        if episode.season_number not in season_map or episode.episode_number > season_map[episode.season_number].episode_number:
            season_map[episode.season_number] = episode

    finales = list(season_map.values())
    finales_avg_rating = statistics.mean([episode.rating for episode in finales])
    finales_avg_vote_count = statistics.mean([episode.vote_count for episode in finales])

    rating_ratio = finales_avg_rating / series_avg_rating
    smooth_constant = 50
    vote_ratio = (finales_avg_vote_count + smooth_constant) / (series_avg_vote_count + smooth_constant)
    voting_ratio = np.log10(vote_ratio + 9) 

    if vote_ratio < 0.25 or series_avg_vote_count < 10:
        return 50.0

    raw_index = (0.7 * rating_ratio) + (0.3 * voting_ratio)

    lower_bound = 0.85
    upper_bound = 1.10
    
    normalized_score = ((raw_index - lower_bound) / (upper_bound - lower_bound)) * 100
    
    return round(max(0.0, min(100.0, normalized_score)), 2)

def getWatchabilityScore(average_rating: float, 
                         binge_index: float, 
                         rating_consistency: float, 
                         momentum_score: float,
                         retention_rate: float,
                         land_the_plane_score: float,
                         episode_count: int,
                         stinker_count: int,
                         highlight_count: int,
                         highlight_rating: float):

    is_serialized = binge_index >= 50
    highlight_density = highlight_count / episode_count

    prestige_factor = min(1.0, max(0.0, (average_rating - 7.5) / 1.0))
    f_weight = 0.25 + (0.50 * prestige_factor)
    p_weight = 1.0 - f_weight

    foundation = (average_rating * 10) * f_weight
    effective_momentum = momentum_score
    if average_rating >= 8.0 and rating_consistency >= 80:
            effective_momentum = max(momentum_score, rating_consistency)

    if is_serialized:
        performance = (land_the_plane_score * 0.70 + effective_momentum * 0.30) * p_weight
    else:
        performance = (land_the_plane_score * 0.30 + effective_momentum * 0.70) * p_weight

    highlight_lift = max(0, highlight_rating - average_rating)
    highlight_bonus = (highlight_density * highlight_lift * 15)

    stamina_mod = np.log10(episode_count + 5)
    altitude_bonus = max(0, (average_rating - 7.7) * 10) * stamina_mod
    retention_bonus = max(0, (retention_rate - 50) / 12)

    trajectory_penalty = 0
    if is_serialized and land_the_plane_score < (average_rating * 10) - 12:
        crash_severity = (average_rating * 10) - land_the_plane_score
        trajectory_penalty = np.sqrt(crash_severity) * 0.85

    tax_multiplier = max(0.4, 1.0 - (average_rating - 7.5)) if average_rating > 7.5 else 1.0
    consistency_tax = ((100 - rating_consistency) * 0.12) * tax_multiplier

    stinker_density = stinker_count / episode_count
    stinker_penalty = (stinker_density * 25) 
    if average_rating >= 8.0: stinker_penalty *= 0.75

    final_score = (
        foundation + 
        performance + 
        altitude_bonus +
        highlight_bonus +
        retention_bonus - 
        trajectory_penalty - 
        consistency_tax - 
        stinker_penalty
    )

    if is_serialized and land_the_plane_score < 55:
        final_score = min(final_score, 74.0)

    watchability_score = round(max(0.0, min(100.0, final_score)), 2)

    return watchability_score

def getShowMetrics(episodes: List[Episode]) -> ShowMetrics:

    ratings = [episode.rating for episode in episodes]
    vote_counts = [episode.vote_count for episode in episodes]
    
    average_rating = statistics.mean(ratings)
    high_rating = max(ratings)
    low_rating = min(ratings)

    stinker_score = getStinkerScore(ratings)
    stinker_episodes = [episode.id for episode in episodes if episode.rating <= stinker_score] 
    stinker_average = statistics.mean([episode.rating for episode in episodes if episode.rating <= stinker_score]) if stinker_episodes else 0.0

    highlight_score = getHighlightScore(ratings)
    highlight_episodes = [episode.id for episode in episodes if episode.rating >= highlight_score]
    highlight_average = statistics.mean([episode.rating for episode in episodes if episode.rating >= highlight_score]) if highlight_episodes else 0.0

    land_the_plane_score = getLandThePlaneScore(ratings)

    momentum_score = getMomentum(ratings)

    rating_consistency = getRatingConsistency(ratings)

    retention_rate = getRetentionRate(vote_counts)

    binge_index = getBingeIndex(episodes)

    watchability_score = getWatchabilityScore(average_rating,
                                              binge_index,
                                              rating_consistency,
                                              momentum_score,
                                              retention_rate,
                                              land_the_plane_score,
                                              len(episodes),
                                              len(stinker_episodes),
                                              len(highlight_episodes),
                                              highlight_average) 


    metrics = ShowMetrics(
        watchability_score = watchability_score,
        average_rating = round(average_rating, 2),
        high_rating = round(high_rating, 2),
        low_rating = round(low_rating, 2),
        stinker_episodes = stinker_episodes,
        stinker_rating = round(stinker_average, 2),
        highlight_episodes = highlight_episodes,
        highlight_rating = round(highlight_average, 2),
        rating_consistency = rating_consistency,
        land_the_plane_score = land_the_plane_score,
        momentum_score = momentum_score,
        retention_rate = retention_rate,
        binge_index = binge_index 
    )

    return metrics

