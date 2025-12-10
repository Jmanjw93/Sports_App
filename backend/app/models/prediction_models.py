"""
Prediction models for game outcomes and player props
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
import numpy as np
import random
from datetime import datetime
from app.models.injury_analyzer import InjuryAnalyzer, TeamInjuryImpact
from app.utils.statistics import StatisticalUtils


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
    injury_impact: Optional[Dict] = None
    coaching_impact: Optional[Dict] = None
    mental_health_impact: Optional[Dict] = None
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
    historical_matchup_data: Optional[Dict] = None  # Historical vs team/coach data


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
        game_id: str = "",
        home_injuries: Optional[List] = None,
        away_injuries: Optional[List] = None,
        sport: str = "nfl"
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
        
        # Calculate base probabilities using proper normalization
        # Convert strengths to log-odds, then to probabilities
        total_strength = home_strength + away_strength
        if total_strength > 0:
            # Use softmax-like normalization for better numerical stability
            home_prob = StatisticalUtils.normalize_probabilities(
                {"home": home_strength, "away": away_strength},
                method="softmax"
            )["home"]
        else:
            home_prob = 0.5
        away_prob = 1.0 - home_prob
        
        # Adjust for weather if outdoor sport (NFL, MLB)
        weather_impact = None
        outdoor_sports = ["nfl", "mlb"]
        if weather_data and sport.lower() in outdoor_sports:
            weather_impact = self._apply_weather_adjustment(
                home_prob, away_prob, weather_data, home_team, away_team
            )
            # Ensure weather data is included in the impact response
            if weather_impact and "weather" not in weather_impact:
                weather_impact["weather"] = weather_data
            home_prob = weather_impact.get("adjusted_home_prob", home_prob)
            away_prob = weather_impact.get("adjusted_away_prob", away_prob)
        
        # Adjust for coaching matchup (head coach vs head coach)
        coaching_matchup = None
        try:
            from app.data.historical_matchups import HistoricalMatchupAnalyzer
            matchup_analyzer = HistoricalMatchupAnalyzer()
            coaching_matchup = matchup_analyzer.analyze_coaching_matchup(
                home_team, away_team, sport
            )
            
            # Apply coaching adjustment using log-odds (more statistically sound)
            coaching_adjustment = coaching_matchup.get("adjustment_factor", 0.0)
            
            # Convert to log-odds, add adjustment, convert back
            home_log_odds = StatisticalUtils.probability_to_log_odds(home_prob)
            home_log_odds += coaching_adjustment * 2.0  # Scale adjustment for log-odds space
            home_prob = StatisticalUtils.log_odds_to_probability(home_log_odds)
            away_prob = 1.0 - home_prob
            
            # Ensure probabilities stay in valid range
            home_prob = max(0.1, min(0.9, home_prob))
            away_prob = 1.0 - home_prob
        except Exception as e:
            # If coaching analysis fails, continue without it
            print(f"Could not analyze coaching matchup: {e}")
        
        # Adjust for player prop insights (key players expected to over/under perform)
        player_prop_adjustment = None
        # This will be populated if player props are analyzed
        
        # Adjust for mental health factors
        mental_health_impact = None
        try:
            from app.models.mental_health_analyzer import MentalHealthAnalyzer
            mental_health_analyzer = MentalHealthAnalyzer()
            
            # Get key players for both teams
            home_key_players = mental_health_analyzer.get_key_players_for_team(home_team, sport)
            away_key_players = mental_health_analyzer.get_key_players_for_team(away_team, sport)
            
            # Mock recent team performance (in production, would fetch from database)
            home_recent_performance = {
                "win_streak": random.randint(0, 5),
                "loss_streak": random.randint(0, 3),
                "recent_form": random.uniform(0.4, 0.9)
            }
            away_recent_performance = {
                "win_streak": random.randint(0, 5),
                "loss_streak": random.randint(0, 3),
                "recent_form": random.uniform(0.4, 0.9)
            }
            
            # Mock team factors (in production, would fetch from database)
            home_team_factors = {
                "is_playoff_game": random.random() < 0.2,
                "playoff_pressure": random.uniform(0.0, 0.8),
                "coaching_stability": random.choice(["stable", "unstable", "new_coach"]),
                "media_pressure": random.uniform(0.0, 0.7)
            }
            away_team_factors = {
                "is_playoff_game": random.random() < 0.2,
                "playoff_pressure": random.uniform(0.0, 0.8),
                "coaching_stability": random.choice(["stable", "unstable", "new_coach"]),
                "media_pressure": random.uniform(0.0, 0.7)
            }
            
            # Analyze mental health for both teams
            home_mental_health = mental_health_analyzer.analyze_team_mental_health(
                home_team, home_key_players, home_recent_performance, home_team_factors, sport
            )
            away_mental_health = mental_health_analyzer.analyze_team_mental_health(
                away_team, away_key_players, away_recent_performance, away_team_factors, sport
            )
            
            # Calculate net adjustment
            net_mental_health_adjustment = (
                home_mental_health.impact_on_win_probability - 
                away_mental_health.impact_on_win_probability
            )
            
            # Apply adjustment to probabilities using log-odds
            home_log_odds = StatisticalUtils.probability_to_log_odds(home_prob)
            home_log_odds += net_mental_health_adjustment * 2.0  # Scale for log-odds space
            home_prob = StatisticalUtils.log_odds_to_probability(home_log_odds)
            away_prob = 1.0 - home_prob
            
            # Ensure probabilities stay in valid range
            home_prob = max(0.1, min(0.9, home_prob))
            away_prob = 1.0 - home_prob
            
            # Prepare mental health impact data
            mental_health_impact = {
                "home_team": {
                    "overall_score": home_mental_health.overall_score,
                    "team_chemistry": home_mental_health.team_chemistry,
                    "morale": home_mental_health.morale,
                    "pressure_handling": home_mental_health.pressure_handling,
                    "impact_on_win_probability": home_mental_health.impact_on_win_probability,
                    "factors": home_mental_health.factors,
                    "key_players": [
                        {
                            "player_name": player.player_name,
                            "position": player.position,
                            "overall_score": player.overall_score,
                            "confidence_level": player.confidence_level,
                            "stress_level": player.stress_level,
                            "focus_level": player.focus_level,
                            "motivation_level": player.motivation_level,
                            "recent_trend": player.recent_trend,
                            "factors": player.factors,
                            "impact_on_performance": player.impact_on_performance
                        }
                        for player in home_mental_health.key_players_mental_health
                    ]
                },
                "away_team": {
                    "overall_score": away_mental_health.overall_score,
                    "team_chemistry": away_mental_health.team_chemistry,
                    "morale": away_mental_health.morale,
                    "pressure_handling": away_mental_health.pressure_handling,
                    "impact_on_win_probability": away_mental_health.impact_on_win_probability,
                    "factors": away_mental_health.factors,
                    "key_players": [
                        {
                            "player_name": player.player_name,
                            "position": player.position,
                            "overall_score": player.overall_score,
                            "confidence_level": player.confidence_level,
                            "stress_level": player.stress_level,
                            "focus_level": player.focus_level,
                            "motivation_level": player.motivation_level,
                            "recent_trend": player.recent_trend,
                            "factors": player.factors,
                            "impact_on_performance": player.impact_on_performance
                        }
                        for player in away_mental_health.key_players_mental_health
                    ]
                },
                "net_adjustment": round(net_mental_health_adjustment, 3),
                "summary": self._generate_mental_health_summary(
                    home_mental_health, away_mental_health, net_mental_health_adjustment
                )
            }
        except Exception as e:
            # If mental health analysis fails, continue without it
            print(f"Could not analyze mental health factors: {e}")
        
        # Adjust for injuries
        injury_adjustment = None
        if home_injuries or away_injuries:
            from app.models.injury_analyzer import InjuryAnalyzer
            injury_analyzer = InjuryAnalyzer()
            
            # Analyze injury impacts
            home_injury_impact = injury_analyzer.analyze_team_injuries(
                home_team, home_injuries or [], home_strength
            )
            away_injury_impact = injury_analyzer.analyze_team_injuries(
                away_team, away_injuries or [], away_strength
            )
            
            # Calculate adjusted probabilities
            injury_adjusted = injury_analyzer.calculate_injury_adjusted_probability(
                home_prob, home_injury_impact, away_injury_impact
            )
            
            home_prob = injury_adjusted["home_probability"]
            away_prob = injury_adjusted["away_probability"]
            
            injury_adjustment = {
                "home_injury_impact": home_injury_impact.total_impact,
                "away_injury_impact": away_injury_impact.total_impact,
                "adjustment": injury_adjusted["injury_adjustment"],
                "home_key_injuries": [
                    {
                        "player": inj.player_name,
                        "team": home_team,
                        "position": inj.position,
                        "injury": inj.injury_type.code,
                        "status": inj.status.code
                    }
                    for inj in home_injury_impact.key_player_injuries
                ],
                "away_key_injuries": [
                    {
                        "player": inj.player_name,
                        "team": away_team,
                        "position": inj.position,
                        "injury": inj.injury_type.code,
                        "status": inj.status.code
                    }
                    for inj in away_injury_impact.key_player_injuries
                ],
                "impact_descriptions": {
                    "home": injury_analyzer.get_injury_impact_description(home_injury_impact),
                    "away": injury_analyzer.get_injury_impact_description(away_injury_impact)
                }
            }
        
        # Determine winner
        # Ensure probabilities sum to 1.0 using proper normalization
        total_prob = home_prob + away_prob
        if abs(total_prob - 1.0) > 0.01:  # Allow small floating point differences
            # Use proper normalization (softmax)
            normalized = StatisticalUtils.normalize_probabilities(
                {"home": home_prob, "away": away_prob},
                method="softmax"
            )
            home_prob = normalized["home"]
            away_prob = normalized["away"]
        
        # Determine predicted winner based on higher probability
        if home_prob > away_prob:
            predicted_winner = home_team
        elif away_prob > home_prob:
            predicted_winner = away_team
        else:
            # If probabilities are equal, default to home team (home advantage)
            predicted_winner = home_team
        
        # Calculate confidence
        confidence = abs(home_prob - away_prob)
        
        # Validate that predicted winner matches higher probability
        if predicted_winner == home_team and away_prob > home_prob:
            # Fix contradiction: away has higher prob but home is predicted
            predicted_winner = away_team
        elif predicted_winner == away_team and home_prob > away_prob:
            # Fix contradiction: home has higher prob but away is predicted
            predicted_winner = home_team
        
        # Key factors
        key_factors = self._identify_key_factors(
            home_stats, away_stats, weather_data
        )
        
        # Update key factors with injury info
        if injury_adjustment:
            if injury_adjustment["home_key_injuries"]:
                key_factors.append(
                    f"Home team injuries: {len(injury_adjustment['home_key_injuries'])} key players affected"
                )
            if injury_adjustment["away_key_injuries"]:
                key_factors.append(
                    f"Away team injuries: {len(injury_adjustment['away_key_injuries'])} key players affected"
                )
        
        # Update key factors with coaching matchup
        if coaching_matchup:
            key_insight = coaching_matchup.get("key_insight", "")
            if key_insight:
                key_factors.append(f"Coaching Matchup: {key_insight}")
        
        # Update key factors with player prop insights
        if player_prop_adjustment:
            if player_prop_adjustment.get("home_advantage"):
                key_factors.append(
                    f"Home team key players expected to outperform based on historical matchups"
                )
            if player_prop_adjustment.get("away_advantage"):
                key_factors.append(
                    f"Away team key players expected to outperform based on historical matchups"
                )
        
        # Update key factors with mental health insights
        if mental_health_impact:
            net_adj = mental_health_impact.get("net_adjustment", 0.0)
            if abs(net_adj) > 0.01:
                if net_adj > 0:
                    key_factors.append(
                        f"Home team mental health advantage: {net_adj*100:.1f}% win probability boost"
                    )
                else:
                    key_factors.append(
                        f"Away team mental health advantage: {abs(net_adj)*100:.1f}% win probability boost"
                    )
        
        # Store coaching matchup in a way that can be included in response
        coaching_impact = None
        if coaching_matchup:
            coaching_impact = {
                "home_coach": coaching_matchup.get("home_coach"),
                "away_coach": coaching_matchup.get("away_coach"),
                "adjustment_factor": coaching_matchup.get("adjustment_factor"),
                "head_coach_adjustment": coaching_matchup.get("head_coach_adjustment", 0.0),
                "coordinator_adjustment": coaching_matchup.get("coordinator_adjustment", 0.0),
                "historical_record": coaching_matchup.get("historical_record"),
                "coordinator_matchup": coaching_matchup.get("coordinator_matchup"),
                "key_insight": coaching_matchup.get("key_insight")
            }
        
        return GamePrediction(
            game_id=game_id,
            home_team=home_team,
            away_team=away_team,
            predicted_winner=predicted_winner,
            home_win_probability=home_prob,
            away_win_probability=away_prob,
            confidence=confidence,
            weather_impact=weather_impact,
            injury_impact=injury_adjustment,
            coaching_impact=coaching_impact,
            mental_health_impact=mental_health_impact,
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
        
        # Get weather analysis
        from app.models.weather_analyzer import WeatherAnalyzer
        weather_analyzer = WeatherAnalyzer()
        impact_analysis = weather_analyzer.analyze_weather_impact(weather, "football")
        
        return {
            "original_home_prob": home_prob,
            "original_away_prob": away_prob,
            "adjusted_home_prob": adjusted_home_prob,
            "adjusted_away_prob": adjusted_away_prob,
            "weather": weather,  # Full weather data
            "weather_impact": impact_analysis,  # Impact analysis
            "adjustment_factor": adjustment
        }
    
    def _generate_mental_health_summary(
        self,
        home_mental_health,
        away_mental_health,
        net_adjustment: float
    ) -> str:
        """Generate a human-readable summary of mental health impact"""
        home_score = home_mental_health.overall_score
        away_score = away_mental_health.overall_score
        
        if abs(net_adjustment) < 0.01:
            return "Mental health factors are relatively balanced between teams"
        
        if net_adjustment > 0:
            if home_score > 0.7:
                return f"Home team has strong mental health ({home_score:.0%} score) with better team chemistry and morale, giving them a {net_adjustment*100:.1f}% advantage"
            else:
                return f"Home team has better mental health positioning ({home_score:.0%} vs {away_score:.0%}), providing a {net_adjustment*100:.1f}% win probability boost"
        else:
            if away_score > 0.7:
                return f"Away team has strong mental health ({away_score:.0%} score) with better team chemistry and morale, giving them a {abs(net_adjustment)*100:.1f}% advantage"
            else:
                return f"Away team has better mental health positioning ({away_score:.0%} vs {home_score:.0%}), providing a {abs(net_adjustment)*100:.1f}% win probability boost"
    
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
    
    def analyze_player_props_for_game(
        self,
        home_team: str,
        away_team: str,
        home_player_props: List[Dict],
        away_player_props: List[Dict]
    ) -> Dict:
        """
        Analyze player props to adjust game win probabilities
        
        Args:
            home_team: Home team name
            away_team: Away team name
            home_player_props: List of home team player props
            away_player_props: List of away team player props
        
        Returns:
            Dictionary with adjustment factors
        """
        # Analyze key players (QB, top RB, top WR)
        home_advantage = 0.0
        away_advantage = 0.0
        
        # Weight by position importance
        position_weights = {
            "QB": 0.40,
            "RB": 0.25,
            "WR": 0.20,
            "TE": 0.15
        }
        
        # Analyze home team props
        for prop in home_player_props:
            position = prop.get("position", "")
            weight = position_weights.get(position, 0.10)
            
            # If player is expected to significantly overperform based on historical matchups
            if "historical_matchup" in prop:
                matchup_factor = prop["historical_matchup"].get("total_adjustment", 0.0)
                # Positive adjustment means player performs better than average
                if matchup_factor > 0.05:  # 5% better
                    home_advantage += weight * min(matchup_factor * 2, 0.10)  # Cap at 10% per player
                elif matchup_factor < -0.05:  # 5% worse
                    home_advantage -= weight * min(abs(matchup_factor) * 2, 0.10)
            
            # Also consider over probability for key props (yards)
            if prop.get("prop_type") in ["passing_yards", "rushing_yards", "receiving_yards"]:
                over_prob = prop.get("over_probability", 0.5)
                if over_prob > 0.65:  # Strong over probability
                    home_advantage += weight * (over_prob - 0.5) * 0.05
                elif over_prob < 0.35:  # Strong under probability
                    home_advantage -= weight * (0.5 - over_prob) * 0.05
        
        # Analyze away team props
        for prop in away_player_props:
            position = prop.get("position", "")
            weight = position_weights.get(position, 0.10)
            
            if "historical_matchup" in prop:
                matchup_factor = prop["historical_matchup"].get("total_adjustment", 0.0)
                if matchup_factor > 0.05:
                    away_advantage += weight * min(matchup_factor * 2, 0.10)
                elif matchup_factor < -0.05:
                    away_advantage -= weight * min(abs(matchup_factor) * 2, 0.10)
            
            if prop.get("prop_type") in ["passing_yards", "rushing_yards", "receiving_yards"]:
                over_prob = prop.get("over_probability", 0.5)
                if over_prob > 0.65:
                    away_advantage += weight * (over_prob - 0.5) * 0.05
                elif over_prob < 0.35:
                    away_advantage -= weight * (0.5 - over_prob) * 0.05
        
        # Net adjustment (relative advantage)
        net_adjustment = home_advantage - away_advantage
        
        # Cap the adjustment to prevent over-weighting
        net_adjustment = max(-0.08, min(0.08, net_adjustment))  # Max 8% swing
        
        return {
            "home_advantage": round(home_advantage, 3),
            "away_advantage": round(away_advantage, 3),
            "net_adjustment": round(net_adjustment, 3),
            "adjustment_applied": True
        }


class PlayerPropPredictor:
    """Predicts player prop bet outcomes"""
    
    def predict_player_prop(
        self,
        player_name: str,
        prop_type: str,
        player_stats: Dict,
        opponent_stats: Dict,
        historical_avg: float,
        line: Optional[float] = None,
        position: Optional[str] = None,
        opponent_team: Optional[str] = None,
        opponent_coach: Optional[str] = None
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
            opponent_team: Opponent team name (for historical matchup)
            opponent_coach: Opponent coach name (for historical matchup)
        
        Returns:
            PlayerPropPrediction object
        """
        # Calculate base matchup factor
        matchup_factor = self._calculate_matchup_factor(
            player_stats, opponent_stats, prop_type
        )
        
        # Predict base value
        base_prediction = player_stats.get(f"{prop_type}_avg", historical_avg)
        
        # Apply historical matchup adjustments if available
        historical_matchup_data = None
        if opponent_team and opponent_coach:
            from app.data.historical_matchups import HistoricalMatchupAnalyzer
            matchup_analyzer = HistoricalMatchupAnalyzer()
            
            matchup_adjustment = matchup_analyzer.calculate_matchup_adjustment(
                player_name, opponent_team, opponent_coach, prop_type, base_prediction
            )
            
            # Use adjusted prediction
            predicted_value = matchup_adjustment["adjusted_prediction"]
            historical_matchup_data = matchup_adjustment
            
            # Boost confidence if we have historical data
            confidence_boost = matchup_adjustment.get("confidence_boost", 0.0)
        else:
            predicted_value = base_prediction * matchup_factor
        
        # Calculate probabilities if line provided
        if line:
            # If we have historical over rate, use it to adjust probability
            if historical_matchup_data:
                historical_over_rate = (
                    historical_matchup_data.get("team_over_rate", 0.5) * 0.6 +
                    historical_matchup_data.get("coach_over_rate", 0.5) * 0.4
                )
                # Blend historical rate with calculated probability
                calculated_over_prob = self._calculate_over_probability(predicted_value, line)
                over_prob = (calculated_over_prob * 0.7) + (historical_over_rate * 0.3)
            else:
                over_prob = self._calculate_over_probability(predicted_value, line)
            under_prob = 1 - over_prob
        else:
            over_prob = 0.5
            under_prob = 0.5
        
        # Confidence based on consistency and historical data
        consistency = player_stats.get("consistency", 0.7)
        base_confidence = min(0.95, consistency * 0.9)
        
        if historical_matchup_data:
            confidence_boost = historical_matchup_data.get("confidence_boost", 0.0)
            confidence = min(0.95, base_confidence + confidence_boost)
        else:
            confidence = base_confidence
        
        return PlayerPropPrediction(
            player_name=player_name,
            prop_type=prop_type,
            predicted_value=predicted_value,
            over_probability=over_prob,
            under_probability=under_prob,
            confidence=confidence,
            historical_avg=historical_avg,
            matchup_factor=matchup_factor,
            historical_matchup_data=historical_matchup_data
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

