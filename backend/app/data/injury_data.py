"""
Injury data collection and management
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from app.models.injury_analyzer import PlayerInjury, InjuryType, InjuryStatus


class InjuryDataCollector:
    """Collects and manages injury data"""
    
    def __init__(self):
        # In production, this would fetch from:
        # - NFL.com injury reports
        # - ESPN injury API
        # - Team official reports
        # - Sports injury databases
        pass
    
    def get_team_injuries(
        self,
        team_name: str,
        sport: str = "nfl"
    ) -> List[PlayerInjury]:
        """
        Get current injuries for a team
        
        Args:
            team_name: Team name
            sport: Sport type
        
        Returns:
            List of PlayerInjury objects
        """
        # Mock injury data - replace with real API
        return self._get_mock_injuries(team_name, sport)
    
    def _get_mock_injuries(
        self,
        team_name: str,
        sport: str = "nfl"
    ) -> List[PlayerInjury]:
        """Generate mock injury data for development"""
        import random
        
        # Sample injuries based on team
        injuries = []
        
        # Common injury scenarios
        if "Eagles" in team_name or "Philadelphia" in team_name:
            injuries.append(PlayerInjury(
                player_name="Jalen Hurts",
                position="QB",
                injury_type=InjuryType.KNEE_INJURY,
                status=InjuryStatus.QUESTIONABLE,
                date_injured=datetime.now() - timedelta(days=3),
                expected_return=datetime.now() + timedelta(days=2),
                is_recurring=False,
                previous_occurrences=0,
                historical_performance_impact=0.0
            ))
        
        if "Chiefs" in team_name or "Kansas City" in team_name:
            injuries.append(PlayerInjury(
                player_name="Travis Kelce",
                position="TE",
                injury_type=InjuryType.ANKLE_SPRAIN,
                status=InjuryStatus.PROBABLE,
                date_injured=datetime.now() - timedelta(days=5),
                expected_return=datetime.now() + timedelta(days=1),
                is_recurring=True,
                previous_occurrences=2,
                historical_performance_impact=0.12  # 12% performance drop in past
            ))
        
        if "Bills" in team_name or "Buffalo" in team_name:
            injuries.append(PlayerInjury(
                player_name="Josh Allen",
                position="QB",
                injury_type=InjuryType.SHOULDER,
                status=InjuryStatus.PROBABLE,
                date_injured=datetime.now() - timedelta(days=7),
                expected_return=datetime.now(),
                is_recurring=False,
                previous_occurrences=0,
                historical_performance_impact=0.0
            ))
        
        # Add some random injuries for realism
        positions = ["RB", "WR", "WR", "OL", "DL", "LB", "CB"]
        injury_types = [
            InjuryType.ANKLE_SPRAIN,
            InjuryType.HAMSTRING,
            InjuryType.SHOULDER,
            InjuryType.GROIN,
            InjuryType.CONCUSSION
        ]
        statuses = [
            InjuryStatus.QUESTIONABLE,
            InjuryStatus.PROBABLE,
            InjuryStatus.DOUBTFUL
        ]
        
        # Add 1-3 additional random injuries
        num_injuries = random.randint(1, 3)
        for i in range(num_injuries):
            pos = random.choice(positions)
            injury_type = random.choice(injury_types)
            status = random.choice(statuses)
            
            injuries.append(PlayerInjury(
                player_name=f"Player {i+1}",
                position=pos,
                injury_type=injury_type,
                status=status,
                date_injured=datetime.now() - timedelta(days=random.randint(1, 10)),
                expected_return=datetime.now() + timedelta(days=random.randint(0, 5)),
                is_recurring=random.choice([True, False]),
                previous_occurrences=random.randint(0, 2) if random.choice([True, False]) else 0,
                historical_performance_impact=random.uniform(0.0, 0.15)
            ))
        
        return injuries
    
    def get_player_injury_history(
        self,
        player_name: str,
        injury_type: InjuryType
    ) -> Dict:
        """
        Get historical performance data for a player with similar injuries
        
        Args:
            player_name: Player name
            injury_type: Type of injury
        
        Returns:
            Dictionary with historical performance data
        """
        # Mock data - in production, query injury/performance database
        import random
        
        return {
            "player_name": player_name,
            "injury_type": injury_type.code,
            "previous_occurrences": random.randint(0, 3),
            "avg_performance_drop": random.uniform(0.10, 0.25),
            "recovery_time_avg": random.randint(7, 21),  # days
            "games_missed_avg": random.randint(1, 4),
            "performance_after_return": random.uniform(0.85, 0.95)  # % of normal
        }




