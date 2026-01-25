from core.metrics import getShowMetrics

class MockEpisode:

    def __init__(self, id, rating, vote_count, season_number=1, episode_number=1):
        self.id = id
        self.rating = rating
        self.vote_count = vote_count
        self.season_number = season_number
        self.episode_number = episode_number

def create_mock_show(ratings, votes=None):
    if votes is None:
        votes = [100] * len(ratings)
        
    mock_episodes = []
    for i, (r, v) in enumerate(zip(ratings, votes)):
        e = MockEpisode(
            id=i + 1000,
            rating=float(r), 
            vote_count=int(v), 
            season_number=1, 
            episode_number=i + 1
        )
        mock_episodes.append(e)
        
    return mock_episodes

def test_masterpiece_score():
    ratings = [9.0, 9.2, 9.1, 9.5, 9.3, 9.4, 9.0, 9.8, 9.9, 10.0]
    episodes = create_mock_show(ratings)
    metrics = getShowMetrics(episodes)
    
    assert metrics.watchability_score > 90
    assert len(metrics.highlight_episodes) > 0

def test_the_crash_penalty():
    ratings = [9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 4.0, 4.0]
    episodes = create_mock_show(ratings)
    metrics = getShowMetrics(episodes)
    
    assert metrics.watchability_score < 75
    assert metrics.land_the_plane_score < 60

def test_momentum_redemption():
    ratings = [9.0] * 10
    episodes = create_mock_show(ratings)
    metrics = getShowMetrics(episodes)
    
    assert metrics.momentum_score == 50.0  
    assert metrics.watchability_score > 90 

def test_stinker_detection():
    ratings = [8.0, 8.2, 8.1, 3.0, 8.0, 8.1]
    episodes = create_mock_show(ratings)
    metrics = getShowMetrics(episodes)
    
    assert len(metrics.stinker_episodes) == 1
    assert metrics.stinker_rating == 3.0

def test_short_show():
    episodes = create_mock_show([8.0, 8.5])
    metrics = getShowMetrics(episodes)
    assert metrics.binge_index == 50.0

def test_zero_votes_retention():
    episodes = [MockEpisode(1, 8.0, 0), MockEpisode(2, 8.0, 10)]
    metrics = getShowMetrics(episodes)
    assert metrics.retention_rate == 0.0

def test_high_variance_consistency():
    ratings = [10.0, 1.0, 10.0, 1.0]
    episodes = create_mock_show(ratings)
    metrics = getShowMetrics(episodes)
    assert metrics.rating_consistency < 50
