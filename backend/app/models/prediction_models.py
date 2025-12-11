"""
Prediction models for game outcomes and player props
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
import numpy as np
from datetime import datetime


@dataclass
class GamePrediction:
    """Game outcome prediction"""
    game_id: str
    home_team: str
    away_team: str
    predicted_winner: str
    home_win_probability: float
    away_win_probability: float
    confidence: float
    weather_impact: Optional[Dict] = None
    key_factors: List[str] = None


@dataclass
class PlayerPropPrediction:
    """Player prop bet prediction"""
    player_name: str
    prop_type: str  # "points", "assists", "rebounds", "yards", "touchdowns", etc.
    predicted_value: float
    over_probability: float
    under_probability: float
    confidence: float
    historical_avg: float
    matchup_factor: float  # How favorable the matchup is


class GamePredictor:
    """Predicts game outcomes using statistical models"""
    
    def __init__(self):
        self.weather_weight = 0.15  # Weather impact weight
        self.home_advantage = 0.03  # Home team advantage
    
    def predict_game(
        self,
        home_team: str,
        away_team: str,
        home_stats: Dict,
        away_stats: Dict,
        weather_data: Optional[Dict] = None,
        game_id: str = ""
    ) -> GamePrediction:
        """
        Predict game outcome
        
        Args:
            home_team: Home team name
            away_team: Away team name
            home_stats: Home team statistics
            away_stats: Away team statistics
            weather_data: Weather conditions
            game_id: Unique game identifier
        
        Returns:
            GamePrediction object
        """
        # Calculate base win probabilities from team stats
        home_strength = self._calculate_team_strength(home_stats)
        away_strength = self._calculate_team_strength(away_stats)
        
        # Apply home advantage
        home_strength += self.home_advantage
        
        # Calculate base probabilities
        total_strength = home_strength + away_strength
        home_prob = home_strength / total_strength if total_strength > 0 else 0.5
        away_prob = 1 - home_prob
        
        # Adjust for weather if outdoor sport
        weather_impact = None
        if weather_data:
            weather_impact = self._apply_weather_adjustment(
                home_prob, away_prob, weather_data, home_team, away_team
            )
            home_prob = weather_impact.get("adjusted_home_prob", home_prob)
            away_prob = weather_impact.get("adjusted_away_prob", away_prob)
        
        # Determine winner
        predicted_winner = home_team if home_prob > away_prob else away_team
        
        # Calculate confidence
        confidence = abs(home_prob - away_prob)
        
        # Key factors
        key_factors = self._identify_key_factors(
            home_stats, away_stats, weather_data
        )
        
        return GamePrediction(
            game_id=game_id,
            home_team=home_team,
            away_team=away_team,
            predicted_winner=predicted_winner,
            home_win_probability=home_prob,
            away_win_probability=away_prob,
            confidence=confidence,
            weather_impact=weather_impact,
            key_factors=key_factors
        )
    
    def _calculate_team_strength(self, stats: Dict) -> float:
        """Calculate overall team strength from statistics"""
        # Weighted combination of key metrics
        win_rate = stats.get("win_rate", 0.5)
        points_per_game = stats.get("points_per_game", 0)
        points_allowed = stats.get("points_allowed_per_game", 0)
        recent_form = stats.get("recent_form", 0.5)  # Last 5-10 games
        
        # Normalize and combine
        strength = (
            win_rate * 0.4 +
            (points_per_game / 100) * 0.3 +
            (1 - points_allowed / 100) * 0.2 +
            recent_form * 0.1
        )
        
        return max(0.1, min(0.9, strength))  # Clamp between 0.1 and 0.9
    
    def _apply_weather_adjustment(
        self,
        home_prob: float,
        away_prob: float,
        weather: Dict,
        home_team: str,
        away_team: str
    ) -> Dict:
        """Adjust probabilities based on weather conditions"""
        impact = {
            "temperature": weather.get("temp", 70),
            "wind_speed": weather.get("wind_speed", 0),
            "precipitation": weather.get("precipitation", 0),
            "conditions": weather.get("conditions", "clear")
        }
        
        adjustment = 0.0
        
        # Extreme cold (< 32F) favors running teams
        if impact["temperature"] < 32:
            adjustment = -0.05  # Slight advantage to better running team
        
        # High wind (> 20 mph) hurts passing
        if impact["wind_speed"] > 20:
            adjustment = -0.08
        
        # Precipitation hurts passing and favors ground game
        if impact["precipitation"] > 0:
            adjustment -= 0.10
        
        # Apply adjustment (simplified - would need team play style data)
        adjusted_home_prob = home_prob + adjustment
        adjusted_away_prob = 1 - adjusted_home_prob
        
        # Normalize
        total = adjusted_home_prob + adjusted_away_prob
        adjusted_home_prob /= total
        adjusted_away_prob /= total
        
        return {
            "original_home_prob": home_prob,
            "original_away_prob": away_prob,
            "adjusted_home_prob": adjusted_home_prob,
            "adjusted_away_prob": adjusted_away_prob,
            "weather_impact": impact,
            "adjustment_factor": adjustment
        }
    
    def _identify_key_factors(
        self,
        home_stats: Dict,
        away_stats: Dict,
        weather: Optional[Dict]
    ) -> List[str]:
        """Identify key factors affecting the game"""
        factors = []
        
        if home_stats.get("win_rate", 0) > away_stats.get("win_rate", 0) + 0.2:
            factors.append("Home team has significantly better record")
        
        if weather and weather.get("wind_speed", 0) > 20:
            factors.append("High wind conditions may affect passing game")
        
        if weather and weather.get("precipitation", 0) > 0:
            factors.append("Precipitation expected - ground game advantage")
        
        return factors


class PlayerPropPredictor:
    """Predicts player prop bet outcomes"""
    
    def predict_player_prop(
        self,
        player_name: str,
        prop_type: str,
        player_stats: Dict,
        opponent_stats: Dict,
        historical_avg: float,
        line: Optional[float] = None
    ) -> PlayerPropPrediction:
        """
        Predict player prop outcome
        
        Args:
            player_name: Player name
            prop_type: Type of prop (points, assists, etc.)
            player_stats: Player's recent statistics
            opponent_stats: Opponent's defensive statistics
            historical_avg: Player's historical average
            line: Betting line (over/under)
        
        Returns:
            PlayerPropPrediction object
        """
        # Calculate matchup factor
        matchup_factor = self._calculate_matchup_factor(
            player_stats, opponent_stats, prop_type
        )
        
        # Predict value
        base_prediction = player_stats.get(f"{prop_type}_avg", historical_avg)
        predicted_value = base_prediction * matchup_factor
        
        # Calculate probabilities if line provided
        if line:
            over_prob = self._calculate_over_probability(predicted_value, line)
            under_prob = 1 - over_prob
        else:
            over_prob = 0.5
            under_prob = 0.5
        
        # Confidence based on consistency
        consistency = player_stats.get("consistency", 0.7)
        confidence = min(0.95, consistency * 0.9)
        
        return PlayerPropPrediction(
            player_name=player_name,
            prop_type=prop_type,
            predicted_value=predicted_value,
            over_probability=over_prob,
            under_probability=under_prob,
            confidence=confidence,
            historical_avg=historical_avg,
            matchup_factor=matchup_factor
        )
    
    def _calculate_matchup_factor(
        self,
        player_stats: Dict,
        opponent_stats: Dict,
        prop_type: str
    ) -> float:
        """Calculate how favorable the matchup is"""
        # Get opponent's defensive rating for this prop type
        opponent_defense = opponent_stats.get(f"defense_vs_{prop_type}", 0.5)
        
        # Factor: 1.0 = neutral, >1.0 = favorable, <1.0 = unfavorable
        matchup_factor = 1.0 + (0.5 - opponent_defense) * 0.3
        
        return max(0.7, min(1.3, matchup_factor))  # Clamp between 0.7 and 1.3
    
    def _calculate_over_probability(
        self,
        predicted_value: float,
        line: float
    ) -> float:
        """Calculate probability of going over the line"""
        # Use normal distribution approximation
        std_dev = predicted_value * 0.15  # Assume 15% standard deviation
        
        if std_dev == 0:
            return 0.5
        
        # Z-score
        z = (line - predicted_value) / std_dev
        
        # Convert to probability (simplified)
        if z < -2:
            return 0.95
        elif z < -1:
            return 0.80
        elif z < 0:
            return 0.65
        elif z < 1:
            return 0.35
        elif z < 2:
            return 0.20
        else:
            return 0.05

