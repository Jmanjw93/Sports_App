"""
Mental health and psychological factors analyzer for game predictions
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import random
import numpy as np


@dataclass
class PlayerMentalHealth:
    """Represents a player's mental health and psychological state"""
    player_name: str
    team: str
    position: str
    overall_score: float  # 0.0 (poor) to 1.0 (excellent)
    confidence_level: float  # Recent performance confidence
    stress_level: float  # 0.0 (low) to 1.0 (high)
    focus_level: float  # 0.0 (distracted) to 1.0 (focused)
    motivation_level: float  # 0.0 (low) to 1.0 (high)
    factors: List[str]  # List of contributing factors
    recent_trend: str  # "improving", "declining", "stable"
    impact_on_performance: float  # -1.0 to 1.0, how much this affects performance


@dataclass
class TeamMentalHealth:
    """Represents team-wide mental health and chemistry"""
    team: str
    overall_score: float  # 0.0 (poor) to 1.0 (excellent)
    team_chemistry: float  # How well team works together
    morale: float  # Team morale level
    pressure_handling: float  # How well team handles pressure
    key_players_mental_health: List[PlayerMentalHealth]
    factors: List[str]
    impact_on_win_probability: float  # Adjustment to win probability


class MentalHealthAnalyzer:
    """Analyzes mental health and psychological factors for predictions"""
    
    def __init__(self):
        self.mental_health_weight = 0.12  # Weight of mental health in predictions
        self.key_player_weight = 0.15  # Weight of key players' mental health
    
    def analyze_player_mental_health(
        self,
        player_name: str,
        team: str,
        position: str,
        recent_performance: Optional[Dict] = None,
        personal_factors: Optional[Dict] = None
    ) -> PlayerMentalHealth:
        """
        Analyze individual player's mental health and psychological state
        
        Factors considered:
        - Recent performance trends
        - Contract status
        - Personal life events
        - Media attention
        - Age/experience
        - Injury recovery (mental aspect)
        """
        # Base scores (mock data - in production, would use real data sources)
        base_confidence = 0.7
        base_stress = 0.3
        base_focus = 0.75
        base_motivation = 0.8
        
        factors = []
        adjustments = []
        
        # Analyze recent performance trend
        if recent_performance:
            recent_games = recent_performance.get("recent_games", [])
            if len(recent_games) >= 3:
                recent_avg = np.mean([g.get("performance_score", 0.5) for g in recent_games[-3:]])
                historical_avg = recent_performance.get("season_avg", 0.5)
                
                if recent_avg > historical_avg * 1.1:
                    adjustments.append(("confidence", 0.15))
                    adjustments.append(("stress", -0.1))
                    factors.append("Strong recent performance boost")
                    recent_trend = "improving"
                elif recent_avg < historical_avg * 0.9:
                    adjustments.append(("confidence", -0.2))
                    adjustments.append(("stress", 0.15))
                    factors.append("Recent performance decline")
                    recent_trend = "declining"
                else:
                    recent_trend = "stable"
            else:
                recent_trend = "stable"
        else:
            recent_trend = "stable"
        
        # Contract status impact
        contract_status = personal_factors.get("contract_status", "stable") if personal_factors else "stable"
        if contract_status == "negotiating":
            adjustments.append(("stress", 0.1))
            adjustments.append(("focus", -0.05))
            factors.append("Contract negotiations ongoing")
        elif contract_status == "expiring_soon":
            adjustments.append(("motivation", 0.1))
            factors.append("Contract year motivation")
        elif contract_status == "recently_signed":
            adjustments.append(("confidence", 0.1))
            adjustments.append(("stress", -0.05))
            factors.append("Recently signed contract")
        
        # Personal life events
        if personal_factors:
            life_events = personal_factors.get("life_events", [])
            for event in life_events:
                event_type = event.get("type", "")
                if event_type == "family_issue":
                    adjustments.append(("focus", -0.15))
                    adjustments.append(("stress", 0.2))
                    factors.append("Family matters affecting focus")
                elif event_type == "positive_life_event":
                    adjustments.append(("motivation", 0.1))
                    adjustments.append(("confidence", 0.05))
                    factors.append("Positive personal developments")
                elif event_type == "media_scrutiny":
                    adjustments.append(("stress", 0.15))
                    adjustments.append(("focus", -0.1))
                    factors.append("Increased media attention")
        
        # Age and experience factor
        age = personal_factors.get("age", 27) if personal_factors else 27
        experience_years = personal_factors.get("experience_years", 5) if personal_factors else 5
        
        if experience_years > 10:
            adjustments.append(("pressure_handling", 0.1))
            factors.append("Veteran experience")
        elif experience_years < 3:
            adjustments.append(("pressure_handling", -0.1))
            factors.append("Young player, less experience")
        
        # Position-specific factors
        if position in ["QB", "PG", "P"]:  # High-pressure positions
            adjustments.append(("stress", 0.1))
            factors.append("High-pressure position")
        
        # Apply adjustments
        confidence = base_confidence
        stress = base_stress
        focus = base_focus
        motivation = base_motivation
        
        for adj_type, adj_value in adjustments:
            if adj_type == "confidence":
                confidence += adj_value
            elif adj_type == "stress":
                stress += adj_value
            elif adj_type == "focus":
                focus += adj_value
            elif adj_type == "motivation":
                motivation += adj_value
        
        # Clamp values to valid ranges
        confidence = max(0.0, min(1.0, confidence))
        stress = max(0.0, min(1.0, stress))
        focus = max(0.0, min(1.0, focus))
        motivation = max(0.0, min(1.0, motivation))
        
        # Calculate overall score
        overall_score = (confidence * 0.3 + (1 - stress) * 0.25 + focus * 0.25 + motivation * 0.2)
        
        # Calculate impact on performance
        # Positive mental health = positive impact, negative = negative impact
        impact_on_performance = (overall_score - 0.5) * 0.3  # Scale to -0.15 to +0.15
        
        return PlayerMentalHealth(
            player_name=player_name,
            team=team,
            position=position,
            overall_score=round(overall_score, 3),
            confidence_level=round(confidence, 3),
            stress_level=round(stress, 3),
            focus_level=round(focus, 3),
            motivation_level=round(motivation, 3),
            factors=factors if factors else ["No significant factors identified"],
            recent_trend=recent_trend,
            impact_on_performance=round(impact_on_performance, 3)
        )
    
    def analyze_team_mental_health(
        self,
        team: str,
        key_players: List[Dict],
        recent_team_performance: Optional[Dict] = None,
        team_factors: Optional[Dict] = None,
        sport: str = "nfl"
    ) -> TeamMentalHealth:
        """
        Analyze team-wide mental health and chemistry
        
        Factors considered:
        - Team chemistry
        - Recent win/loss streak
        - Playoff pressure
        - Key player mental health
        - Coaching stability
        - Media pressure
        """
        # Analyze key players' mental health
        key_players_mental_health = []
        key_player_impacts = []
        
        for player in key_players:
            player_name = player.get("name", "")
            position = player.get("position", "")
            
            # Mock recent performance data
            recent_performance = {
                "recent_games": [
                    {"performance_score": random.uniform(0.4, 0.9)},
                    {"performance_score": random.uniform(0.4, 0.9)},
                    {"performance_score": random.uniform(0.4, 0.9)}
                ],
                "season_avg": random.uniform(0.5, 0.8)
            }
            
            # Mock personal factors
            personal_factors = {
                "contract_status": random.choice(["stable", "negotiating", "expiring_soon", "recently_signed"]),
                "age": random.randint(22, 35),
                "experience_years": random.randint(1, 15),
                "life_events": []
            }
            
            # Add some random life events
            if random.random() < 0.3:
                personal_factors["life_events"].append({
                    "type": random.choice(["family_issue", "positive_life_event", "media_scrutiny"]),
                    "severity": random.uniform(0.1, 0.5)
                })
            
            player_mh = self.analyze_player_mental_health(
                player_name, team, position, recent_performance, personal_factors
            )
            key_players_mental_health.append(player_mh)
            key_player_impacts.append(player_mh.impact_on_performance)
        
        # Calculate average key player impact
        avg_key_player_impact = np.mean(key_player_impacts) if key_player_impacts else 0.0
        
        # Team-level factors
        base_chemistry = 0.75
        base_morale = 0.7
        base_pressure_handling = 0.65
        
        team_factors_list = []
        adjustments = []
        
        # Recent win/loss streak
        if recent_team_performance:
            win_streak = recent_team_performance.get("win_streak", 0)
            loss_streak = recent_team_performance.get("loss_streak", 0)
            
            if win_streak >= 3:
                adjustments.append(("morale", 0.15))
                adjustments.append(("chemistry", 0.1))
                team_factors_list.append(f"{win_streak}-game winning streak")
            elif loss_streak >= 3:
                adjustments.append(("morale", -0.2))
                adjustments.append(("confidence", -0.15))
                team_factors_list.append(f"{loss_streak}-game losing streak")
        
        # Playoff pressure
        if team_factors:
            is_playoff_game = team_factors.get("is_playoff_game", False)
            playoff_pressure = team_factors.get("playoff_pressure", 0.0)
            
            if is_playoff_game:
                if playoff_pressure > 0.7:
                    adjustments.append(("pressure_handling", -0.15))
                    team_factors_list.append("High playoff pressure")
                else:
                    adjustments.append(("motivation", 0.1))
                    team_factors_list.append("Playoff game motivation")
        
        # Coaching stability
        if team_factors:
            coaching_stability = team_factors.get("coaching_stability", "stable")
            if coaching_stability == "unstable":
                adjustments.append(("chemistry", -0.1))
                adjustments.append(("morale", -0.1))
                team_factors_list.append("Coaching instability")
            elif coaching_stability == "new_coach":
                adjustments.append(("chemistry", -0.05))
                team_factors_list.append("New coaching staff")
        
        # Media pressure
        if team_factors:
            media_pressure = team_factors.get("media_pressure", 0.0)
            if media_pressure > 0.6:
                adjustments.append(("stress", 0.1))
                team_factors_list.append("High media scrutiny")
        
        # Apply adjustments
        chemistry = base_chemistry
        morale = base_morale
        pressure_handling = base_pressure_handling
        
        for adj_type, adj_value in adjustments:
            if adj_type == "chemistry":
                chemistry += adj_value
            elif adj_type == "morale":
                morale += adj_value
            elif adj_type == "pressure_handling":
                pressure_handling += adj_value
        
        # Clamp values
        chemistry = max(0.0, min(1.0, chemistry))
        morale = max(0.0, min(1.0, morale))
        pressure_handling = max(0.0, min(1.0, pressure_handling))
        
        # Calculate overall team mental health score
        team_score = (chemistry * 0.3 + morale * 0.3 + pressure_handling * 0.2 + 
                     (1 + avg_key_player_impact) * 0.2)
        team_score = max(0.0, min(1.0, team_score))
        
        # Calculate impact on win probability
        # Combine team factors with key player impacts
        team_impact = (team_score - 0.5) * self.mental_health_weight
        key_player_impact = avg_key_player_impact * self.key_player_weight
        
        total_impact = team_impact + key_player_impact
        
        return TeamMentalHealth(
            team=team,
            overall_score=round(team_score, 3),
            team_chemistry=round(chemistry, 3),
            morale=round(morale, 3),
            pressure_handling=round(pressure_handling, 3),
            key_players_mental_health=key_players_mental_health,
            factors=team_factors_list if team_factors_list else ["No significant team factors"],
            impact_on_win_probability=round(total_impact, 3)
        )
    
    def get_key_players_for_team(self, team: str, sport: str = "nfl") -> List[Dict]:
        """
        Get key players for a team (mock data - in production, would fetch from database)
        """
        # Mock key players based on sport
        if sport.lower() == "nfl":
            positions = ["QB", "RB", "WR", "TE", "DE", "LB", "CB"]
        elif sport.lower() == "nba":
            positions = ["PG", "SG", "SF", "PF", "C"]
        elif sport.lower() == "mlb":
            positions = ["P", "C", "1B", "2B", "SS", "3B", "OF"]
        elif sport.lower() == "nhl":
            positions = ["C", "LW", "RW", "D", "G"]
        else:
            positions = ["Player"]
        
        # Return 3-5 key players
        num_players = random.randint(3, 5)
        key_players = []
        
        for i in range(num_players):
            key_players.append({
                "name": f"{team} Player {i+1}",
                "position": random.choice(positions)
            })
        
        return key_players

