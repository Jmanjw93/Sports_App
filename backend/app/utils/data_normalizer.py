"""
Data normalization utilities for consistent data handling
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
import re


class DataNormalizer:
    """Normalize and validate sports data"""
    
    # Team name mappings for consistency
    TEAM_NAME_MAPPINGS = {
        "nfl": {
            "KC": "Kansas City Chiefs",
            "BUF": "Buffalo Bills",
            "PHI": "Philadelphia Eagles",
            "LAR": "Los Angeles Rams",
            "SF": "San Francisco 49ers",
            "SEA": "Seattle Seahawks",
            "MIA": "Miami Dolphins",
            "NYJ": "New York Jets",
            "BAL": "Baltimore Ravens",
            "PIT": "Pittsburgh Steelers",
            "GB": "Green Bay Packers",
            "CHI": "Chicago Bears",
            "DET": "Detroit Lions",
            "MIN": "Minnesota Vikings",
            "CLE": "Cleveland Browns",
            "CIN": "Cincinnati Bengals",
            "DAL": "Dallas Cowboys",
            "NE": "New England Patriots",
            "NYG": "New York Giants",
            "TB": "Tampa Bay Buccaneers",
            "ATL": "Atlanta Falcons",
            "ARI": "Arizona Cardinals",
            "LV": "Las Vegas Raiders",
            "DEN": "Denver Broncos",
            "TEN": "Tennessee Titans",
            "JAX": "Jacksonville Jaguars",
            "NO": "New Orleans Saints",
            "CAR": "Carolina Panthers",
            "IND": "Indianapolis Colts",
            "HOU": "Houston Texans",
            "WAS": "Washington Commanders",
        },
        "nba": {
            "LAL": "Los Angeles Lakers",
            "BOS": "Boston Celtics",
            "GSW": "Golden State Warriors",
            "MIL": "Milwaukee Bucks",
            "DEN": "Denver Nuggets",
            "PHX": "Phoenix Suns",
            "MIA": "Miami Heat",
            "NYK": "New York Knicks",
            "DAL": "Dallas Mavericks",
            "CHI": "Chicago Bulls",
        },
        "mlb": {
            "NYY": "New York Yankees",
            "BOS": "Boston Red Sox",
            "LAD": "Los Angeles Dodgers",
            "SF": "San Francisco Giants",
            "CHC": "Chicago Cubs",
            "STL": "St. Louis Cardinals",
            "HOU": "Houston Astros",
            "TEX": "Texas Rangers",
            "ATL": "Atlanta Braves",
            "PHI": "Philadelphia Phillies",
        },
        "nhl": {
            "TOR": "Toronto Maple Leafs",
            "BOS": "Boston Bruins",
            "MTL": "Montreal Canadiens",
            "NYR": "New York Rangers",
            "EDM": "Edmonton Oilers",
            "VAN": "Vancouver Canucks",
            "CHI": "Chicago Blackhawks",
            "DET": "Detroit Red Wings",
            "PIT": "Pittsburgh Penguins",
            "WSH": "Washington Capitals",
        }
    }
    
    @staticmethod
    def normalize_team_name(team_name: str, sport: str = "nfl") -> str:
        """
        Normalize team name to standard format
        
        Args:
            team_name: Team name (can be abbreviation or full name)
            sport: Sport type
        
        Returns:
            Normalized team name
        """
        if not team_name:
            return ""
        
        team_name = team_name.strip()
        
        # Check if it's an abbreviation
        mappings = DataNormalizer.TEAM_NAME_MAPPINGS.get(sport, {})
        if team_name.upper() in mappings:
            return mappings[team_name.upper()]
        
        # Check if abbreviation is in the name
        for abbrev, full_name in mappings.items():
            if abbrev in team_name.upper():
                return full_name
        
        # Return as-is if no mapping found
        return team_name
    
    @staticmethod
    def normalize_game_data(game_data: Dict) -> Dict:
        """
        Normalize game data structure
        
        Args:
            game_data: Raw game data
        
        Returns:
            Normalized game data
        """
        normalized = {
            "game_id": game_data.get("game_id", ""),
            "sport": game_data.get("sport", "nfl").lower(),
            "home_team": DataNormalizer.normalize_team_name(
                game_data.get("home_team", ""),
                game_data.get("sport", "nfl")
            ),
            "away_team": DataNormalizer.normalize_team_name(
                game_data.get("away_team", ""),
                game_data.get("sport", "nfl")
            ),
            "date": DataNormalizer.normalize_date(game_data.get("date")),
            "venue": game_data.get("venue", ""),
            "location": DataNormalizer.normalize_location(game_data.get("location", {})),
            "status": game_data.get("status", "scheduled"),
        }
        
        # Add optional fields
        if "week" in game_data:
            normalized["week"] = game_data["week"]
        if "home_score" in game_data:
            normalized["home_score"] = game_data["home_score"]
        if "away_score" in game_data:
            normalized["away_score"] = game_data["away_score"]
        
        return normalized
    
    @staticmethod
    def normalize_date(date_str: Optional[str]) -> Optional[str]:
        """
        Normalize date string to ISO format
        
        Args:
            date_str: Date string in various formats
        
        Returns:
            ISO format date string or None
        """
        if not date_str:
            return None
        
        try:
            # Try parsing various formats
            formats = [
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M:%S.%f",
                "%Y-%m-%dT%H:%M:%S%z",
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d",
            ]
            
            for fmt in formats:
                try:
                    dt = datetime.strptime(date_str.replace("Z", "+00:00"), fmt)
                    return dt.isoformat()
                except:
                    continue
            
            # If all fail, try parsing as timestamp
            try:
                timestamp = float(date_str)
                dt = datetime.fromtimestamp(timestamp)
                return dt.isoformat()
            except:
                pass
            
            return date_str  # Return as-is if can't parse
        except Exception:
            return date_str
    
    @staticmethod
    def normalize_location(location: Dict) -> Dict:
        """
        Normalize location data
        
        Args:
            location: Location dictionary
        
        Returns:
            Normalized location dictionary
        """
        normalized = {
            "city": location.get("city", "").strip(),
            "state": location.get("state", "").strip().upper()[:2],
            "country": location.get("country", "US").strip().upper(),
        }
        
        # Add coordinates if available
        if "lat" in location:
            normalized["lat"] = float(location["lat"])
        if "lon" in location:
            normalized["lon"] = float(location["lon"])
        
        return normalized
    
    @staticmethod
    def normalize_team_stats(stats: Dict, sport: str = "nfl") -> Dict:
        """
        Normalize team statistics
        
        Args:
            stats: Team statistics dictionary
            sport: Sport type
        
        Returns:
            Normalized statistics dictionary
        """
        normalized = {
            "team_name": DataNormalizer.normalize_team_name(
                stats.get("team_name", ""),
                sport
            ),
            "win_rate": DataNormalizer.clamp_float(stats.get("win_rate", 0.5), 0.0, 1.0),
            "points_per_game": max(0.0, float(stats.get("points_per_game", 0))),
            "points_allowed_per_game": max(0.0, float(stats.get("points_allowed_per_game", 0))),
            "recent_form": DataNormalizer.clamp_float(stats.get("recent_form", 0.5), 0.0, 1.0),
        }
        
        # Normalize records
        if "home_record" in stats:
            normalized["home_record"] = {
                "wins": max(0, int(stats["home_record"].get("wins", 0))),
                "losses": max(0, int(stats["home_record"].get("losses", 0))),
            }
        
        if "away_record" in stats:
            normalized["away_record"] = {
                "wins": max(0, int(stats["away_record"].get("wins", 0))),
                "losses": max(0, int(stats["away_record"].get("losses", 0))),
            }
        
        # Add optional fields
        if "strength_of_schedule" in stats:
            normalized["strength_of_schedule"] = DataNormalizer.clamp_float(
                stats["strength_of_schedule"], 0.0, 1.0
            )
        
        return normalized
    
    @staticmethod
    def normalize_player_stats(stats: Dict, sport: str = "nfl") -> Dict:
        """
        Normalize player statistics
        
        Args:
            stats: Player statistics dictionary
            sport: Sport type
        
        Returns:
            Normalized statistics dictionary
        """
        normalized = {
            "player_name": stats.get("player_name", "").strip(),
            "position": stats.get("position", "").strip().upper(),
            "consistency": DataNormalizer.clamp_float(stats.get("consistency", 0.7), 0.0, 1.0),
            "recent_trend": float(stats.get("recent_trend", 0.0)),
        }
        
        # Add position-specific stats
        for key, value in stats.items():
            if key not in ["player_name", "position", "consistency", "recent_trend"]:
                if isinstance(value, (int, float)):
                    normalized[key] = float(value)
                else:
                    normalized[key] = value
        
        return normalized
    
    @staticmethod
    def normalize_weather_data(weather: Dict) -> Dict:
        """
        Normalize weather data
        
        Args:
            weather: Weather data dictionary
        
        Returns:
            Normalized weather dictionary
        """
        normalized = {
            "temp": float(weather.get("temp", 70)),
            "wind_speed": max(0.0, float(weather.get("wind_speed", 0))),
            "precipitation": max(0.0, float(weather.get("precipitation", 0))),
            "conditions": weather.get("conditions", "clear").lower(),
        }
        
        # Add optional fields
        if "humidity" in weather:
            normalized["humidity"] = DataNormalizer.clamp_float(weather["humidity"], 0.0, 100.0)
        if "location" in weather:
            normalized["location"] = weather["location"]
        
        return normalized
    
    @staticmethod
    def clamp_float(value: Any, min_val: float, max_val: float) -> float:
        """
        Clamp float value between min and max
        
        Args:
            value: Value to clamp
            min_val: Minimum value
            max_val: Maximum value
        
        Returns:
            Clamped float value
        """
        try:
            val = float(value)
            return max(min_val, min(max_val, val))
        except (ValueError, TypeError):
            return min_val
    
    @staticmethod
    def validate_game_id(game_id: str) -> bool:
        """
        Validate game ID format
        
        Args:
            game_id: Game ID string
        
        Returns:
            True if valid
        """
        if not game_id:
            return False
        
        # Format: sport_index_timestamp or sport_team1_team2_date
        pattern = r'^[a-z]+_\d+(_\d+)?$'
        return bool(re.match(pattern, game_id.lower()))

