"""
Sports data collection from various APIs
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import requests
from app.config import settings


class SportsDataCollector:
    """Collects sports data from APIs"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.SPORTS_API_KEY
        # Using TheSportsDB (free, no API key needed) and API-Football as fallback
        self.thesportsdb_base = "https://www.thesportsdb.com/api/v1/json/3"
        self.api_football_base = "https://v3.football.api-sports.io"
    
    def get_upcoming_games(
        self,
        sport: str = "nfl",
        days_ahead: int = 7
    ) -> List[Dict]:
        """
        Get upcoming games for a sport
        
        Args:
            sport: Sport type (nfl, nba, mlb, etc.)
            days_ahead: Number of days to look ahead
        
        Returns:
            List of game dictionaries
        """
        # Try to get real data first
        if sport == "nfl":
            real_games = self._get_real_nfl_games(days_ahead)
            if real_games:
                return real_games
        elif sport == "nba":
            real_games = self._get_real_nba_games(days_ahead)
            if real_games:
                return real_games
        elif sport == "mlb":
            real_games = self._get_real_mlb_games(days_ahead)
            if real_games:
                return real_games
        elif sport == "nhl":
            real_games = self._get_real_nhl_games(days_ahead)
            if real_games:
                return real_games
        
        # Fallback to mock data if API fails
        return self._get_mock_games(sport, days_ahead)
    
    def _get_real_nfl_games(self, days_ahead: int) -> Optional[List[Dict]]:
        """Get real NFL games from schedule data"""
        try:
            from app.data.nfl_schedule import get_nfl_games_for_period
            
            now = datetime.now()
            end_date = now + timedelta(days=days_ahead)
            
            # Get games from the schedule data
            games = get_nfl_games_for_period(now, end_date)
            
            # Filter to only future games
            filtered_games = [
                game for game in games
                if datetime.fromisoformat(game["date"]) > now
            ]
            
            if filtered_games:
                return filtered_games
                
        except Exception as e:
            print(f"Error fetching real NFL games: {e}")
            import traceback
            traceback.print_exc()
        
        return None
    
    def _get_real_nba_games(self, days_ahead: int) -> Optional[List[Dict]]:
        """Get real NBA games from schedule data"""
        try:
            from app.data.nba_schedule import get_nba_games_for_period
            
            now = datetime.now()
            end_date = now + timedelta(days=days_ahead)
            
            games = get_nba_games_for_period(now, end_date)
            
            filtered_games = [
                game for game in games
                if datetime.fromisoformat(game["date"]) > now
            ]
            
            if filtered_games:
                return filtered_games
                
        except Exception as e:
            print(f"Error fetching real NBA games: {e}")
            import traceback
            traceback.print_exc()
        
        return None
    
    def _get_real_mlb_games(self, days_ahead: int) -> Optional[List[Dict]]:
        """Get real MLB games from schedule data"""
        try:
            from app.data.mlb_schedule import get_mlb_games_for_period
            
            now = datetime.now()
            end_date = now + timedelta(days=days_ahead)
            
            games = get_mlb_games_for_period(now, end_date)
            
            filtered_games = [
                game for game in games
                if datetime.fromisoformat(game["date"]) > now
            ]
            
            if filtered_games:
                return filtered_games
                
        except Exception as e:
            print(f"Error fetching real MLB games: {e}")
            import traceback
            traceback.print_exc()
        
        return None
    
    def _get_real_nhl_games(self, days_ahead: int) -> Optional[List[Dict]]:
        """Get real NHL games from schedule data"""
        try:
            from app.data.nhl_schedule import get_nhl_games_for_period
            
            now = datetime.now()
            end_date = now + timedelta(days=days_ahead)
            
            games = get_nhl_games_for_period(now, end_date)
            
            filtered_games = [
                game for game in games
                if datetime.fromisoformat(game["date"]) > now
            ]
            
            if filtered_games:
                return filtered_games
                
        except Exception as e:
            print(f"Error fetching real NHL games: {e}")
            import traceback
            traceback.print_exc()
        
        return None
    
    def get_team_stats(
        self,
        team_name: str,
        sport: str = "nfl"
    ) -> Dict:
        """
        Get team statistics
        
        Args:
            team_name: Team name
            sport: Sport type
        
        Returns:
            Dictionary with team statistics
        """
        # Mock data - replace with real API
        return self._get_mock_team_stats(team_name, sport)
    
    def get_team_players(
        self,
        team_name: str,
        sport: str = "nfl"
    ) -> List[Dict]:
        """
        Get key players for a team
        
        Args:
            team_name: Team name
            sport: Sport type
        
        Returns:
            List of player dictionaries with name and position
        """
        # Mock data - replace with real API
        return self._get_mock_team_players(team_name, sport)
    
    def _get_mock_team_players(
        self,
        team_name: str,
        sport: str = "nfl"
    ) -> List[Dict]:
        """Generate mock team players"""
        import random
        
        if sport == "nfl":
            # Common player names by team
            team_players = {
                "Kansas City Chiefs": [
                    {"name": "Patrick Mahomes", "position": "QB"},
                    {"name": "Travis Kelce", "position": "TE"},
                    {"name": "Isiah Pacheco", "position": "RB"},
                    {"name": "Rashee Rice", "position": "WR"},
                    {"name": "Marquez Valdes-Scantling", "position": "WR"},
                ],
                "Buffalo Bills": [
                    {"name": "Josh Allen", "position": "QB"},
                    {"name": "Stefon Diggs", "position": "WR"},
                    {"name": "James Cook", "position": "RB"},
                    {"name": "Dalton Kincaid", "position": "TE"},
                    {"name": "Gabe Davis", "position": "WR"},
                ],
                "Philadelphia Eagles": [
                    {"name": "Jalen Hurts", "position": "QB"},
                    {"name": "A.J. Brown", "position": "WR"},
                    {"name": "DeVonta Smith", "position": "WR"},
                    {"name": "D'Andre Swift", "position": "RB"},
                    {"name": "Dallas Goedert", "position": "TE"},
                ],
                "Los Angeles Chargers": [
                    {"name": "Justin Herbert", "position": "QB"},
                    {"name": "Keenan Allen", "position": "WR"},
                    {"name": "Austin Ekeler", "position": "RB"},
                    {"name": "Mike Williams", "position": "WR"},
                    {"name": "Gerald Everett", "position": "TE"},
                ],
            }
            
            # Return players for team or default
            if team_name in team_players:
                return team_players[team_name]
            else:
                # Generate default players
                positions = ["QB", "RB", "WR", "WR", "TE"]
                return [
                    {"name": f"{team_name.split()[-1]} Player {i+1}", "position": pos}
                    for i, pos in enumerate(positions)
                ]
        elif sport == "nba":
            # NBA players by team
            team_players = {
                "Los Angeles Lakers": [
                    {"name": "LeBron James", "position": "SF"},
                    {"name": "Anthony Davis", "position": "PF"},
                    {"name": "D'Angelo Russell", "position": "PG"},
                    {"name": "Austin Reaves", "position": "SG"},
                    {"name": "Rui Hachimura", "position": "PF"},
                ],
                "Boston Celtics": [
                    {"name": "Jayson Tatum", "position": "SF"},
                    {"name": "Jaylen Brown", "position": "SG"},
                    {"name": "Kristaps Porzingis", "position": "C"},
                    {"name": "Derrick White", "position": "PG"},
                    {"name": "Jrue Holiday", "position": "PG"},
                ],
                "Golden State Warriors": [
                    {"name": "Stephen Curry", "position": "PG"},
                    {"name": "Klay Thompson", "position": "SG"},
                    {"name": "Draymond Green", "position": "PF"},
                    {"name": "Andrew Wiggins", "position": "SF"},
                    {"name": "Kevon Looney", "position": "C"},
                ],
            }
            if team_name in team_players:
                return team_players[team_name]
            else:
                positions = ["PG", "SG", "SF", "PF", "C"]
                return [
                    {"name": f"{team_name.split()[-1]} Player {i+1}", "position": positions[i]}
                    for i in range(5)
                ]
        elif sport == "mlb":
            # MLB players by team
            team_players = {
                "New York Yankees": [
                    {"name": "Aaron Judge", "position": "OF"},
                    {"name": "Giancarlo Stanton", "position": "OF"},
                    {"name": "Gerrit Cole", "position": "P"},
                    {"name": "Anthony Rizzo", "position": "1B"},
                    {"name": "Gleyber Torres", "position": "2B"},
                ],
                "Boston Red Sox": [
                    {"name": "Rafael Devers", "position": "3B"},
                    {"name": "Triston Casas", "position": "1B"},
                    {"name": "Masataka Yoshida", "position": "OF"},
                    {"name": "Chris Sale", "position": "P"},
                    {"name": "Trevor Story", "position": "SS"},
                ],
                "Los Angeles Dodgers": [
                    {"name": "Mookie Betts", "position": "OF"},
                    {"name": "Freddie Freeman", "position": "1B"},
                    {"name": "Shohei Ohtani", "position": "DH"},
                    {"name": "Will Smith", "position": "C"},
                    {"name": "Walker Buehler", "position": "P"},
                ],
            }
            if team_name in team_players:
                return team_players[team_name]
            else:
                positions = ["P", "C", "1B", "2B", "OF"]
                return [
                    {"name": f"{team_name.split()[-1]} Player {i+1}", "position": positions[i]}
                    for i in range(5)
                ]
        elif sport == "nhl":
            # NHL players by team
            team_players = {
                "Toronto Maple Leafs": [
                    {"name": "Auston Matthews", "position": "C"},
                    {"name": "Mitch Marner", "position": "RW"},
                    {"name": "William Nylander", "position": "RW"},
                    {"name": "John Tavares", "position": "C"},
                    {"name": "Morgan Rielly", "position": "D"},
                ],
                "Boston Bruins": [
                    {"name": "Brad Marchand", "position": "LW"},
                    {"name": "David Pastrnak", "position": "RW"},
                    {"name": "Patrice Bergeron", "position": "C"},
                    {"name": "Charlie McAvoy", "position": "D"},
                    {"name": "Linus Ullmark", "position": "G"},
                ],
                "Edmonton Oilers": [
                    {"name": "Connor McDavid", "position": "C"},
                    {"name": "Leon Draisaitl", "position": "C"},
                    {"name": "Evan Bouchard", "position": "D"},
                    {"name": "Zach Hyman", "position": "LW"},
                    {"name": "Stuart Skinner", "position": "G"},
                ],
            }
            if team_name in team_players:
                return team_players[team_name]
            else:
                positions = ["C", "LW", "RW", "D", "G"]
                return [
                    {"name": f"{team_name.split()[-1]} Player {i+1}", "position": positions[i]}
                    for i in range(5)
                ]
        else:
            return [
                {"name": f"Player {i+1}", "position": "PG" if i == 0 else "SG" if i == 1 else "SF"}
                for i in range(5)
            ]
    
    def get_player_stats(
        self,
        player_name: str,
        sport: str = "nfl"
    ) -> Dict:
        """
        Get player statistics
        
        Args:
            player_name: Player name
            sport: Sport type
        
        Returns:
            Dictionary with player statistics
        """
        # Mock data - replace with real API
        return self._get_mock_player_stats(player_name, sport)
    
    def get_game_details(
        self,
        game_id: str
    ) -> Optional[Dict]:
        """
        Get detailed information about a specific game
        
        Args:
            game_id: Unique game identifier
        
        Returns:
            Game details dictionary
        """
        # Get the actual games list to ensure consistency
        # Parse game_id to get sport
        parts = game_id.split('_')
        sport = parts[0] if parts else "nfl"
        
        # Get all games for this sport
        games_list = self.get_upcoming_games(sport, days_ahead=14)
        
        # Find the game by matching game_id
        for game in games_list:
            if game["game_id"] == game_id:
                return game
        
        # Fallback to old method if not found
        return self._get_mock_game_details(game_id)
    
    def _get_mock_games(self, sport: str, days_ahead: int) -> List[Dict]:
        """Generate mock game data"""
        games = []
        # Get current date/time
        now = datetime.now()
        # Start from tomorrow to ensure all dates are in the future
        tomorrow = (now + timedelta(days=1)).replace(hour=13, minute=0, second=0, microsecond=0)
        
        # Calculate this week's Sunday and next week's Sunday (used for week labeling)
        now_weekday = now.weekday()  # 0=Monday, 6=Sunday
        days_until_sunday = (6 - now_weekday) % 7
        if days_until_sunday == 0:
            days_until_sunday = 7  # Next week if today is Sunday
        this_week_sunday = tomorrow + timedelta(days=days_until_sunday - 1)
        next_week_sunday = this_week_sunday + timedelta(days=7)
        
        # Real NFL games for this week and next week
        if sport == "nfl":
            
            # NFL Week 14-15 games (December 2025)
            teams = []
            
            # Add today's game - Philadelphia Eagles vs Los Angeles Rams (Monday Night Football)
            # Always add tonight's game if it's Monday
            if now_weekday == 0:  # Monday Night Football
                today_game_time = now.replace(hour=20, minute=20, second=0, microsecond=0)
                # Always add tonight's game (even if time has passed, show it)
                teams.append(("Los Angeles Rams", "Philadelphia Eagles", today_game_time))
            elif now_weekday == 3:  # Thursday Night Football
                today_game_time = now.replace(hour=20, minute=20, second=0, microsecond=0)
                if today_game_time > now:
                    teams.append(("New York Giants", "Dallas Cowboys", today_game_time))
            elif now_weekday == 6:  # Sunday
                today_game_time = now.replace(hour=13, minute=0, second=0, microsecond=0)
                if today_game_time > now:
                    teams.append(("New York Giants", "Dallas Cowboys", today_game_time))
            
            # This Week (Week 14) - Sunday games
            teams.extend([
                ("Kansas City Chiefs", "Buffalo Bills", this_week_sunday),
                ("San Francisco 49ers", "Seattle Seahawks", this_week_sunday),
                ("Miami Dolphins", "New York Jets", this_week_sunday),
                ("Baltimore Ravens", "Pittsburgh Steelers", this_week_sunday),
                ("Green Bay Packers", "Chicago Bears", this_week_sunday),
                ("Detroit Lions", "Minnesota Vikings", this_week_sunday),
                ("Cleveland Browns", "Cincinnati Bengals", this_week_sunday),
            ])
            
            # This Week - Monday Night Football
            teams.append(("Dallas Cowboys", "Philadelphia Eagles", this_week_sunday + timedelta(days=1)))
            
            # Next Week (Week 15) - Sunday games
            teams.extend([
                ("New England Patriots", "New York Giants", next_week_sunday),
                ("Tampa Bay Buccaneers", "Atlanta Falcons", next_week_sunday),
                ("Los Angeles Rams", "Arizona Cardinals", next_week_sunday),
                ("Las Vegas Raiders", "Denver Broncos", next_week_sunday),
                ("Tennessee Titans", "Jacksonville Jaguars", next_week_sunday),
                ("New Orleans Saints", "Carolina Panthers", next_week_sunday),
                ("Indianapolis Colts", "Houston Texans", next_week_sunday),
            ])
            
            # Next Week - Monday Night Football
            teams.append(("Washington Commanders", "New York Jets", next_week_sunday + timedelta(days=1)))
        elif sport == "nba":
            # NBA games - spread across this week
            teams = [
                ("Los Angeles Lakers", "Boston Celtics", tomorrow + timedelta(days=1)),
                ("Golden State Warriors", "Milwaukee Bucks", tomorrow + timedelta(days=2)),
                ("Denver Nuggets", "Phoenix Suns", tomorrow + timedelta(days=3)),
                ("Miami Heat", "New York Knicks", tomorrow + timedelta(days=4)),
                ("Dallas Mavericks", "Chicago Bulls", tomorrow + timedelta(days=5)),
            ]
        elif sport == "mlb":
            # MLB games
            teams = [
                ("New York Yankees", "Boston Red Sox", tomorrow + timedelta(days=1)),
                ("Los Angeles Dodgers", "San Francisco Giants", tomorrow + timedelta(days=2)),
                ("Chicago Cubs", "St. Louis Cardinals", tomorrow + timedelta(days=3)),
                ("Houston Astros", "Texas Rangers", tomorrow + timedelta(days=4)),
                ("Atlanta Braves", "Philadelphia Phillies", tomorrow + timedelta(days=5)),
            ]
        elif sport == "nhl":
            # NHL games
            teams = [
                ("Toronto Maple Leafs", "Boston Bruins", tomorrow + timedelta(days=1)),
                ("Montreal Canadiens", "New York Rangers", tomorrow + timedelta(days=2)),
                ("Edmonton Oilers", "Vancouver Canucks", tomorrow + timedelta(days=3)),
                ("Chicago Blackhawks", "Detroit Red Wings", tomorrow + timedelta(days=4)),
                ("Pittsburgh Penguins", "Washington Capitals", tomorrow + timedelta(days=5)),
            ]
        else:
            teams = [
                ("Team A", "Team B", tomorrow + timedelta(days=1)),
                ("Team C", "Team D", tomorrow + timedelta(days=2)),
            ]
        
        for i, game_info in enumerate(teams):
            # Handle both old format (tuple of 2) and new format (tuple of 3 with date)
            if len(game_info) == 3:
                home, away, game_date = game_info
                # Ensure time is set to 1:00 PM (or 8:20 PM for Monday Night)
                if game_date.weekday() == 0:  # Monday
                    game_date = game_date.replace(hour=20, minute=20, second=0, microsecond=0)  # 8:20 PM for MNF
                else:
                    game_date = game_date.replace(hour=13, minute=0, second=0, microsecond=0)  # 1:00 PM for Sunday
            else:
                # Fallback for other sports or old format
                home, away = game_info
                days_ahead = i + 1
                game_date = tomorrow + timedelta(days=days_ahead - 1)
                game_date = game_date.replace(hour=13, minute=0, second=0, microsecond=0)
            
            # Ensure it's always in the future (safety check)
            if game_date <= now:
                game_date = tomorrow + timedelta(days=1)
            
            # Determine which week this game belongs to
            game_date_only = game_date.date()
            now_date_only = now.date()
            
            # Check if it's today first
            if game_date_only == now_date_only:
                week_label = "Today"
            else:
                # Week is based on the Sunday of that week
                game_weekday = game_date.weekday()
                days_to_sunday = (game_weekday - 6) % 7
                week_sunday = game_date - timedelta(days=days_to_sunday)
                week_sunday_date = week_sunday.date()
                
                # Determine if it's this week or next week
                if week_sunday_date == this_week_sunday.date():
                    week_label = "This Week"
                elif week_sunday_date == next_week_sunday.date():
                    week_label = "Next Week"
                else:
                    week_label = f"Week of {week_sunday.strftime('%B %d')}"
            
            games.append({
                "game_id": f"{sport}_{i+1}_{int(game_date.timestamp())}",
                "sport": sport,
                "home_team": home,
                "away_team": away,
                "date": game_date.isoformat(),
                "venue": f"{home} Stadium",
                "week": week_label,
                "location": {
                    "city": home.split()[-1] if " " in home else "Unknown",
                    "state": "CA",
                    "country": "US"
                }
            })
        
        return games
    
    def _get_mock_team_stats(self, team_name: str, sport: str) -> Dict:
        """Generate mock team statistics"""
        import random
        
        if sport == "nfl":
            return {
                "team_name": team_name,
                "win_rate": round(random.uniform(0.4, 0.8), 3),
                "points_per_game": round(random.uniform(20, 35), 1),
                "points_allowed_per_game": round(random.uniform(15, 28), 1),
                "recent_form": round(random.uniform(0.3, 0.9), 2),
                "home_record": {"wins": random.randint(4, 8), "losses": random.randint(0, 3)},
                "away_record": {"wins": random.randint(3, 7), "losses": random.randint(1, 4)},
                "strength_of_schedule": round(random.uniform(0.4, 0.7), 2)
            }
        elif sport == "nba":
            return {
                "team_name": team_name,
                "win_rate": round(random.uniform(0.4, 0.8), 3),
                "points_per_game": round(random.uniform(105, 120), 1),
                "points_allowed_per_game": round(random.uniform(105, 115), 1),
                "recent_form": round(random.uniform(0.3, 0.9), 2),
                "home_record": {"wins": random.randint(15, 25), "losses": random.randint(0, 10)},
                "away_record": {"wins": random.randint(12, 22), "losses": random.randint(5, 15)}
            }
        else:
            return {
                "team_name": team_name,
                "win_rate": round(random.uniform(0.4, 0.8), 3),
                "points_per_game": round(random.uniform(4, 6), 1),
                "points_allowed_per_game": round(random.uniform(3, 5), 1),
                "recent_form": round(random.uniform(0.3, 0.9), 2)
            }
    
    def _get_mock_player_stats(self, player_name: str, sport: str) -> Dict:
        """Generate mock player statistics (season averages)"""
        import random
        
        if sport == "nfl":
            # Determine position from player name or use defaults
            position = "QB"
            if any(name in player_name for name in ["Kelce", "Kincaid", "Goedert", "Everett"]):
                position = "TE"
            elif any(name in player_name for name in ["Pacheco", "Cook", "Swift", "Ekeler"]):
                position = "RB"
            elif any(name in player_name for name in ["Diggs", "Brown", "Smith", "Allen", "Rice", "Williams", "Davis"]):
                position = "WR"
            
            stats = {
                "player_name": player_name,
                "position": position,
                "consistency": round(random.uniform(0.65, 0.85), 2),
                "recent_trend": round(random.uniform(-0.15, 0.15), 2)
            }
            
            # Position-specific stats (season averages per game)
            if position == "QB":
                stats.update({
                    "yards_avg": round(random.uniform(240, 280), 1),  # Passing yards per game
                    "touchdowns_avg": round(random.uniform(1.8, 2.5), 1),  # Passing TDs per game
                    "points_avg": round(random.uniform(18, 25), 1)
                })
            elif position == "RB":
                stats.update({
                    "yards_avg": round(random.uniform(70, 100), 1),  # Rushing yards per game
                    "touchdowns_avg": round(random.uniform(0.6, 1.2), 1),  # Rushing TDs per game
                    "receptions_avg": round(random.uniform(2, 4), 1),  # Receptions per game
                    "receiving_yards_avg": round(random.uniform(15, 30), 1)  # Receiving yards per game
                })
            elif position == "WR" or position == "TE":
                stats.update({
                    "yards_avg": round(random.uniform(55, 85), 1),  # Receiving yards per game
                    "touchdowns_avg": round(random.uniform(0.4, 0.9), 1),  # Receiving TDs per game
                    "receptions_avg": round(random.uniform(4, 7), 1)  # Receptions per game
                })
            else:
                stats.update({
                    "yards_avg": round(random.uniform(50, 80), 1),
                    "touchdowns_avg": round(random.uniform(0.5, 1.0), 1),
                    "points_avg": round(random.uniform(10, 18), 1)
                })
            
            return stats
        elif sport == "nba":
            # Determine position from player name or use defaults
            position = "PG"
            if any(name in player_name for name in ["James", "Tatum", "Wiggins", "Hachimura"]):
                position = "SF"
            elif any(name in player_name for name in ["Davis", "Porzingis", "Green", "Looney"]):
                position = "PF" if "Looney" not in player_name else "C"
            elif any(name in player_name for name in ["Curry", "Russell", "White", "Holiday"]):
                position = "PG"
            elif any(name in player_name for name in ["Brown", "Thompson", "Reaves"]):
                position = "SG"
            
            stats = {
                "player_name": player_name,
                "position": position,
                "points_avg": round(random.uniform(15, 30), 1),
                "assists_avg": round(random.uniform(3, 10), 1),
                "rebounds_avg": round(random.uniform(4, 12), 1),
                "consistency": round(random.uniform(0.6, 0.9), 2),
                "recent_trend": round(random.uniform(-0.1, 0.2), 2)
            }
            
            # Position-specific adjustments
            if position == "PG":
                stats["assists_avg"] = round(random.uniform(6, 12), 1)
            elif position == "C":
                stats["rebounds_avg"] = round(random.uniform(8, 15), 1)
            
            return stats
        elif sport == "mlb":
            # Determine position from player name or use defaults
            position = "OF"
            if any(name in player_name for name in ["Cole", "Sale", "Buehler"]):
                position = "P"
            elif any(name in player_name for name in ["Smith"]):
                position = "C"
            elif any(name in player_name for name in ["Rizzo", "Casas", "Freeman"]):
                position = "1B"
            elif any(name in player_name for name in ["Torres", "Story"]):
                position = "2B" if "Torres" in player_name else "SS"
            elif any(name in player_name for name in ["Devers"]):
                position = "3B"
            
            stats = {
                "player_name": player_name,
                "position": position,
                "consistency": round(random.uniform(0.6, 0.85), 2),
                "recent_trend": round(random.uniform(-0.1, 0.15), 2)
            }
            
            if position == "P":
                stats.update({
                    "era": round(random.uniform(2.5, 4.5), 2),
                    "strikeouts_avg": round(random.uniform(6, 10), 1),
                    "wins_avg": round(random.uniform(0.5, 0.8), 2)
                })
            else:
                stats.update({
                    "batting_avg": round(random.uniform(0.250, 0.320), 3),
                    "home_runs_avg": round(random.uniform(0.2, 0.5), 2),
                    "rbis_avg": round(random.uniform(0.5, 1.2), 1),
                    "hits_avg": round(random.uniform(1.0, 1.8), 1)
                })
            
            return stats
        elif sport == "nhl":
            # Determine position from player name or use defaults
            position = "C"
            if any(name in player_name for name in ["Matthews", "McDavid", "Draisaitl", "Bergeron", "Tavares"]):
                position = "C"
            elif any(name in player_name for name in ["Marchand", "Hyman"]):
                position = "LW"
            elif any(name in player_name for name in ["Marner", "Nylander", "Pastrnak"]):
                position = "RW"
            elif any(name in player_name for name in ["Rielly", "McAvoy", "Bouchard"]):
                position = "D"
            elif any(name in player_name for name in ["Ullmark", "Skinner"]):
                position = "G"
            
            stats = {
                "player_name": player_name,
                "position": position,
                "consistency": round(random.uniform(0.65, 0.9), 2),
                "recent_trend": round(random.uniform(-0.1, 0.2), 2)
            }
            
            if position == "G":
                stats.update({
                    "save_percentage": round(random.uniform(0.900, 0.950), 3),
                    "goals_against_avg": round(random.uniform(2.0, 3.0), 2),
                    "saves_avg": round(random.uniform(25, 35), 1)
                })
            else:
                stats.update({
                    "goals_avg": round(random.uniform(0.3, 0.8), 2),
                    "assists_avg": round(random.uniform(0.4, 1.0), 2),
                    "points_avg": round(random.uniform(0.7, 1.5), 2),
                    "shots_avg": round(random.uniform(2.5, 4.5), 1)
                })
            
            return stats
        else:
            return {
                "player_name": player_name,
                "points_avg": round(random.uniform(0.5, 1.5), 1),
                "consistency": round(random.uniform(0.6, 0.9), 2)
            }
    
    def _get_mock_game_details(self, game_id: str) -> Dict:
        """Generate mock game details based on game_id"""
        # Parse game_id to extract sport and index
        # Format: {sport}_{index}_{timestamp}
        parts = game_id.split('_')
        if len(parts) >= 2:
            sport = parts[0]
            try:
                index = int(parts[1]) - 1  # Convert to 0-based index
            except ValueError:
                index = 0
        else:
            sport = "nfl"
            index = 0
        
        # Use the same logic as _get_mock_games to get teams
        # This ensures consistency
        now = datetime.now()
        tomorrow = (now + timedelta(days=1)).replace(hour=13, minute=0, second=0, microsecond=0)
        now_weekday = now.weekday()
        days_until_sunday = (6 - now_weekday) % 7
        if days_until_sunday == 0:
            days_until_sunday = 7
        this_week_sunday = tomorrow + timedelta(days=days_until_sunday - 1)
        next_week_sunday = this_week_sunday + timedelta(days=7)
        
        # Get the teams for this sport (must match _get_mock_games exactly)
        if sport == "nfl":
            # Calculate this week's Sunday and next week's Sunday
            now = datetime.now()
            tomorrow = (now + timedelta(days=1)).replace(hour=13, minute=0, second=0, microsecond=0)
            now_weekday = now.weekday()
            days_until_sunday = (6 - now_weekday) % 7
            if days_until_sunday == 0:
                days_until_sunday = 7
            this_week_sunday = tomorrow + timedelta(days=days_until_sunday - 1)
            next_week_sunday = this_week_sunday + timedelta(days=7)
            
            # Build teams list matching _get_mock_games
            teams_list = []
            
            # Add today's game first if it's Monday
            if now_weekday == 0:  # Monday
                today_game_time = now.replace(hour=20, minute=20, second=0, microsecond=0)
                teams_list.append(("Los Angeles Rams", "Philadelphia Eagles", today_game_time))
            
            # This Week (Week 14) - Sunday games
            teams_list.extend([
                ("Kansas City Chiefs", "Buffalo Bills", this_week_sunday),
                ("San Francisco 49ers", "Seattle Seahawks", this_week_sunday),
                ("Miami Dolphins", "New York Jets", this_week_sunday),
                ("Baltimore Ravens", "Pittsburgh Steelers", this_week_sunday),
                ("Green Bay Packers", "Chicago Bears", this_week_sunday),
                ("Detroit Lions", "Minnesota Vikings", this_week_sunday),
                ("Cleveland Browns", "Cincinnati Bengals", this_week_sunday),
            ])
            
            # This Week - Monday Night Football (next Monday, not today)
            if now_weekday != 0:  # Only add if today is not Monday
                teams_list.append(("Dallas Cowboys", "Philadelphia Eagles", this_week_sunday + timedelta(days=1)))
            
            # Next Week (Week 15) - Sunday games
            teams_list.extend([
                ("New England Patriots", "New York Giants", next_week_sunday),
                ("Tampa Bay Buccaneers", "Atlanta Falcons", next_week_sunday),
                ("Los Angeles Rams", "Arizona Cardinals", next_week_sunday),
                ("Las Vegas Raiders", "Denver Broncos", next_week_sunday),
                ("Tennessee Titans", "Jacksonville Jaguars", next_week_sunday),
                ("New Orleans Saints", "Carolina Panthers", next_week_sunday),
                ("Indianapolis Colts", "Houston Texans", next_week_sunday),
            ])
            
            # Next Week - Monday Night Football
            teams_list.append(("Washington Commanders", "New York Jets", next_week_sunday + timedelta(days=1)))
            
            teams = teams_list
        elif sport == "nba":
            # Calculate dates for NBA games
            now_nba = datetime.now()
            tomorrow_nba = (now_nba + timedelta(days=1)).replace(hour=13, minute=0, second=0, microsecond=0)
            teams = [
                ("Los Angeles Lakers", "Boston Celtics", tomorrow_nba + timedelta(days=2)),
                ("Golden State Warriors", "Milwaukee Bucks", tomorrow_nba + timedelta(days=3)),
                ("Denver Nuggets", "Phoenix Suns", tomorrow_nba + timedelta(days=4)),
            ]
        else:
            now_other = datetime.now()
            tomorrow_other = (now_other + timedelta(days=1)).replace(hour=13, minute=0, second=0, microsecond=0)
            teams = [
                ("Team A", "Team B", tomorrow_other + timedelta(days=1)),
                ("Team C", "Team D", tomorrow_other + timedelta(days=2)),
            ]
        
        # Get teams and date for this game, with bounds checking
        if 0 <= index < len(teams):
            game_info = teams[index]
            if len(game_info) == 3:
                home_team, away_team, game_date = game_info
                # Ensure time is set correctly
                if game_date.weekday() == 0:  # Monday
                    game_date = game_date.replace(hour=20, minute=20, second=0, microsecond=0)
                else:
                    game_date = game_date.replace(hour=13, minute=0, second=0, microsecond=0)
            else:
                home_team, away_team = game_info
                # Fallback date calculation
                now = datetime.now()
                tomorrow = (now + timedelta(days=1)).replace(hour=13, minute=0, second=0, microsecond=0)
                days_ahead = index + 1
                game_date = tomorrow + timedelta(days=days_ahead - 1)
        else:
            home_team, away_team = teams[0] if teams else ("Team A", "Team B")
            # Fallback date
            now = datetime.now()
            tomorrow = (now + timedelta(days=1)).replace(hour=13, minute=0, second=0, microsecond=0)
            game_date = tomorrow
        
        # Try to extract date from game_id timestamp if available
        if len(parts) >= 3:
            try:
                timestamp = int(parts[2])
                game_date_from_id = datetime.fromtimestamp(timestamp)
                # Use the date from game_id if it's valid
                if game_date_from_id > datetime.now():
                    game_date = game_date_from_id
                    if game_date.weekday() == 0:  # Monday
                        game_date = game_date.replace(hour=20, minute=20, second=0, microsecond=0)
                    else:
                        game_date = game_date.replace(hour=13, minute=0, second=0, microsecond=0)
            except (ValueError, OSError):
                pass  # Use the date we already calculated
        
        # Get city from home team name
        city = home_team.split()[-1] if " " in home_team else "Unknown"
        
        return {
            "game_id": game_id,
            "sport": sport,
            "home_team": home_team,
            "away_team": away_team,
            "date": game_date.isoformat(),
            "venue": f"{home_team} Stadium",
            "location": {
                "city": city,
                "state": "CA",
                "country": "US",
                "lat": 39.0489,
                "lon": -94.4839
            }
        }

