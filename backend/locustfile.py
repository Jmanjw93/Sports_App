"""
Locust load testing configuration for Sports Analytics API
"""
from locust import HttpUser, task, between
import random


class SportsAnalyticsUser(HttpUser):
    """Simulated user for load testing"""
    wait_time = between(1, 3)  # Wait 1-3 seconds between requests
    
    # Common game IDs for testing
    nfl_game_ids = [
        "nfl_1_1734567890",
        "nfl_2_1734567891",
        "nfl_3_1734567892",
        "nfl_4_1734567893",
        "nfl_5_1734567894",
    ]
    
    nba_game_ids = [
        "nba_1_1734567890",
        "nba_2_1734567891",
        "nba_3_1734567892",
    ]
    
    sports = ["nfl", "nba", "mlb", "nhl"]
    
    def on_start(self):
        """Called when a user starts"""
        # Health check
        self.client.get("/health")
    
    @task(3)
    def get_upcoming_games(self):
        """Get upcoming games"""
        sport = random.choice(self.sports)
        self.client.get(f"/api/games/upcoming?sport={sport}&days_ahead=7")
    
    @task(5)
    def get_game_prediction(self):
        """Get game prediction (most common operation)"""
        game_id = random.choice(self.nfl_game_ids + self.nba_game_ids)
        self.client.get(f"/api/predictions/game/{game_id}")
    
    @task(2)
    def get_player_prop_prediction(self):
        """Get player prop prediction"""
        players = [
            "Patrick Mahomes",
            "Josh Allen",
            "LeBron James",
            "Stephen Curry",
            "Travis Kelce"
        ]
        player = random.choice(players)
        prop_types = ["points", "yards", "touchdowns", "assists", "rebounds"]
        prop_type = random.choice(prop_types)
        self.client.get(f"/api/predictions/player/{player}?prop_type={prop_type}")
    
    @task(1)
    def get_odds(self):
        """Get betting odds"""
        sport = random.choice(self.sports)
        self.client.get(f"/api/odds?sport={sport}")
    
    @task(1)
    def get_bets(self):
        """Get betting recommendations"""
        sport = random.choice(self.sports)
        self.client.get(f"/api/bets/recommendations?sport={sport}")
    
    @task(1)
    def get_health(self):
        """Health check"""
        self.client.get("/health")
    
    @task(1)
    def get_metrics(self):
        """Prometheus metrics (for monitoring)"""
        self.client.get("/metrics")


# Configuration for different load scenarios
class LightLoadUser(SportsAnalyticsUser):
    """Light load scenario"""
    wait_time = between(2, 5)


class HeavyLoadUser(SportsAnalyticsUser):
    """Heavy load scenario"""
    wait_time = between(0.5, 1.5)


class SpikeLoadUser(SportsAnalyticsUser):
    """Spike load scenario"""
    wait_time = between(0.1, 0.5)

