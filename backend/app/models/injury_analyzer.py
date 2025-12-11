"""
Injury analysis and impact on team performance
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum


class InjuryType(Enum):
    """Types of injuries and their severity"""
    # Lower body
    ANKLE_SPRAIN = ("ankle_sprain", 0.15, "Lower body mobility")
    KNEE_INJURY = ("knee_injury", 0.35, "Lower body mobility, speed")
    HAMSTRING = ("hamstring", 0.25, "Speed, acceleration")
    GROIN = ("groin", 0.20, "Lateral movement")
    FOOT = ("foot", 0.30, "Balance, cutting")
    ACHILLES = ("achilles", 0.40, "Explosiveness, speed")
    
    # Upper body
    SHOULDER = ("shoulder", 0.25, "Throwing, blocking")
    ELBOW = ("elbow", 0.20, "Throwing accuracy")
    WRIST = ("wrist", 0.15, "Catching, ball handling")
    HAND = ("hand", 0.10, "Catching, ball security")
    RIB = ("rib", 0.30, "Breathing, contact tolerance")
    
    # Head/Neck
    CONCUSSION = ("concussion", 0.35, "Decision making, reaction time")
    NECK = ("neck", 0.30, "Head movement, vision")
    
    # General
    ILLNESS = ("illness", 0.20, "Endurance, energy")
    GENERAL = ("general", 0.15, "Overall performance")
    
    def __init__(self, code: str, impact: float, description: str):
        self.code = code
        self.impact = impact
        self.description = description


class InjuryStatus(Enum):
    """Injury status levels"""
    OUT = ("out", 1.0)  # 100% impact
    DOUBTFUL = ("doubtful", 0.75)  # 75% impact
    QUESTIONABLE = ("questionable", 0.50)  # 50% impact
    PROBABLE = ("probable", 0.25)  # 25% impact
    ACTIVE = ("active", 0.0)  # No impact
    
    def __init__(self, code: str, impact_multiplier: float):
        self.code = code
        self.impact_multiplier = impact_multiplier


@dataclass
class PlayerInjury:
    """Represents a player injury"""
    player_name: str
    position: str
    injury_type: InjuryType
    status: InjuryStatus
    date_injured: datetime
    expected_return: Optional[datetime] = None
    is_recurring: bool = False
    previous_occurrences: int = 0
    historical_performance_impact: float = 0.0  # How much performance dropped in past


@dataclass
class TeamInjuryImpact:
    """Impact of injuries on team performance"""
    team_name: str
    total_impact: float  # 0.0 to 1.0
    key_player_injuries: List[PlayerInjury]
    position_impacts: Dict[str, float]  # Impact by position
    win_probability_adjustment: float  # How much to adjust win probability


class InjuryAnalyzer:
    """Analyzes injuries and their impact on team performance"""
    
    def __init__(self):
        # Position importance weights (how much each position matters)
        self.position_weights = {
            "QB": 0.30,  # Quarterback is most important
            "RB": 0.15,
            "WR": 0.12,
            "TE": 0.08,
            "OL": 0.10,  # Offensive line
            "DL": 0.08,  # Defensive line
            "LB": 0.08,
            "CB": 0.06,
            "S": 0.03,
        }
        
        # Default weight if position not found
        self.default_position_weight = 0.05
    
    def analyze_team_injuries(
        self,
        team_name: str,
        injuries: List[PlayerInjury],
        team_strength: float
    ) -> TeamInjuryImpact:
        """
        Analyze how injuries affect a team's performance
        
        Args:
            team_name: Team name
            injuries: List of player injuries
            team_strength: Base team strength (0.0 to 1.0)
        
        Returns:
            TeamInjuryImpact with adjustments
        """
        if not injuries:
            return TeamInjuryImpact(
                team_name=team_name,
                total_impact=0.0,
                key_player_injuries=[],
                position_impacts={},
                win_probability_adjustment=0.0
            )
        
        # Calculate impact for each injury
        total_impact = 0.0
        position_impacts = {}
        key_injuries = []
        
        for injury in injuries:
            # Get position weight
            position_weight = self.position_weights.get(
                injury.position, 
                self.default_position_weight
            )
            
            # Calculate injury impact
            base_impact = injury.injury_type.impact
            status_multiplier = injury.status.impact_multiplier
            
            # Adjust for recurring injuries (worse if recurring)
            recurring_factor = 1.2 if injury.is_recurring else 1.0
            
            # Use historical performance if available
            if injury.historical_performance_impact > 0:
                historical_factor = injury.historical_performance_impact
            else:
                historical_factor = base_impact
            
            # Calculate total impact for this player
            player_impact = (
                base_impact * 
                status_multiplier * 
                recurring_factor * 
                historical_factor * 
                position_weight
            )
            
            total_impact += player_impact
            
            # Track by position
            if injury.position not in position_impacts:
                position_impacts[injury.position] = 0.0
            position_impacts[injury.position] += player_impact
            
            # Track key injuries (high impact)
            if player_impact > 0.05:  # Significant impact
                key_injuries.append(injury)
        
        # Cap total impact at 0.5 (50% reduction max)
        total_impact = min(total_impact, 0.5)
        
        # Calculate win probability adjustment
        # Negative adjustment means lower win probability
        win_prob_adjustment = -total_impact * team_strength
        
        return TeamInjuryImpact(
            team_name=team_name,
            total_impact=total_impact,
            key_player_injuries=key_injuries,
            position_impacts=position_impacts,
            win_probability_adjustment=win_prob_adjustment
        )
    
    def get_injury_impact_description(
        self,
        impact: TeamInjuryImpact
    ) -> List[str]:
        """Get human-readable description of injury impacts"""
        descriptions = []
        
        if impact.total_impact == 0:
            return ["No significant injuries"]
        
        if impact.total_impact > 0.3:
            descriptions.append("Severe injury impact - multiple key players affected")
        elif impact.total_impact > 0.15:
            descriptions.append("Moderate injury impact - some key players affected")
        else:
            descriptions.append("Minor injury impact")
        
        # Describe position impacts
        for position, pos_impact in sorted(
            impact.position_impacts.items(), 
            key=lambda x: x[1], 
            reverse=True
        ):
            if pos_impact > 0.05:
                descriptions.append(
                    f"{position} position significantly impacted "
                    f"({pos_impact:.1%} reduction)"
                )
        
        # Describe key injuries
        for injury in impact.key_player_injuries[:3]:  # Top 3
            descriptions.append(
                f"{injury.player_name} ({injury.position}) - "
                f"{injury.status.code.upper()}: {injury.injury_type.description}"
            )
        
        return descriptions
    
    def calculate_injury_adjusted_probability(
        self,
        base_probability: float,
        home_injuries: TeamInjuryImpact,
        away_injuries: TeamInjuryImpact
    ) -> Dict[str, float]:
        """
        Calculate win probabilities adjusted for injuries
        
        Args:
            base_probability: Base win probability (home team)
            home_injuries: Home team injury impact
            away_injuries: Away team injury impact
        
        Returns:
            Dictionary with adjusted probabilities
        """
        # Adjust based on relative injury impact
        # If home team has more injuries, reduce their probability
        # If away team has more injuries, increase home probability
        
        injury_differential = away_injuries.total_impact - home_injuries.total_impact
        
        # Adjust probability (injury differential can shift by up to 10%)
        adjustment = injury_differential * 0.20  # Max 10% swing
        
        adjusted_home_prob = base_probability + adjustment
        adjusted_away_prob = 1.0 - adjusted_home_prob
        
        # Ensure probabilities stay in valid range
        adjusted_home_prob = max(0.1, min(0.9, adjusted_home_prob))
        adjusted_away_prob = 1.0 - adjusted_home_prob
        
        return {
            "home_probability": adjusted_home_prob,
            "away_probability": adjusted_away_prob,
            "injury_adjustment": adjustment,
            "home_injury_impact": home_injuries.total_impact,
            "away_injury_impact": away_injuries.total_impact
        }




