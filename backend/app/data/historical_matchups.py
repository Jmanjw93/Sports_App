"""
Historical matchup data for players vs teams and coaches
"""
from typing import Dict, List, Optional
from datetime import datetime
import random


class HistoricalMatchupAnalyzer:
    """Analyzes historical performance of players against specific teams and coaches"""
    
    def __init__(self):
        # In production, this would query a database of historical game data
        # For now, we'll use mock data that simulates realistic patterns
        pass
    
    def get_player_vs_team_history(
        self,
        player_name: str,
        opponent_team: str,
        prop_type: str,
        sport: str = "nfl"
    ) -> Dict:
        """
        Get historical performance of a player against a specific team
        
        Args:
            player_name: Player name
            opponent_team: Opponent team name
            prop_type: Type of prop (passing_yards, rushing_yards, etc.)
            sport: Sport type
        
        Returns:
            Dictionary with historical matchup statistics
        """
        # In production, this would query historical game logs
        # For now, generate realistic mock data based on player and team
        
        # Create a deterministic seed based on player and team names
        # This ensures consistent results for the same matchup
        seed = hash(f"{player_name}_{opponent_team}_{prop_type}") % 1000
        random.seed(seed)
        
        # Generate historical matchup data
        # Simulate 3-5 previous matchups
        num_games = random.randint(3, 5)
        games = []
        total_value = 0
        
        # Base performance varies by matchup
        # Some players perform better/worse against certain teams
        matchup_factor = random.uniform(0.85, 1.15)  # 15% variance
        
        for i in range(num_games):
            # Simulate game performance with some variance
            # Base on typical performance for the prop type
            if prop_type == "passing_yards":
                base_avg = 250
                game_value = base_avg * matchup_factor * random.uniform(0.75, 1.25)
            elif prop_type == "rushing_yards":
                base_avg = 80
                game_value = base_avg * matchup_factor * random.uniform(0.70, 1.30)
            elif prop_type == "receiving_yards":
                base_avg = 60
                game_value = base_avg * matchup_factor * random.uniform(0.65, 1.35)
            else:
                base_avg = 50
                game_value = base_avg * matchup_factor * random.uniform(0.75, 1.25)
            
            games.append({
                "game_date": f"202{random.randint(2, 4)}-{random.randint(9, 12):02d}-{random.randint(1, 28):02d}",
                "value": round(game_value, 1),
                "over_line": random.choice([True, False])
            })
            total_value += game_value
        
        avg_value = total_value / num_games if num_games > 0 else 0
        over_rate = sum(1 for g in games if g["over_line"]) / num_games if num_games > 0 else 0.5
        
        return {
            "player_name": player_name,
            "opponent_team": opponent_team,
            "prop_type": prop_type,
            "num_games": num_games,
            "average_value": round(avg_value, 1),
            "over_rate": round(over_rate, 3),
            "games": games,
            "matchup_factor": round(matchup_factor, 3),  # How this matchup affects performance
            "trend": "improving" if games[-1]["value"] > avg_value else "declining" if len(games) > 1 else "stable"
        }
    
    def get_player_vs_coach_history(
        self,
        player_name: str,
        opponent_coach: str,
        prop_type: str,
        sport: str = "nfl"
    ) -> Dict:
        """
        Get historical performance of a player against a specific coach's defense
        
        Args:
            player_name: Player name
            opponent_coach: Opponent defensive coordinator or head coach
            prop_type: Type of prop
            sport: Sport type
        
        Returns:
            Dictionary with historical performance vs coach
        """
        # Create deterministic seed
        seed = hash(f"{player_name}_{opponent_coach}_{prop_type}") % 1000
        random.seed(seed)
        
        # Some coaches have specific defensive schemes that affect certain players differently
        num_games = random.randint(2, 4)  # Fewer games vs same coach
        games = []
        total_value = 0
        
        # Coach-specific factor (some coaches scheme better against certain players)
        coach_factor = random.uniform(0.80, 1.20)  # 20% variance
        
        for i in range(num_games):
            if prop_type == "passing_yards":
                base_avg = 250
                game_value = base_avg * coach_factor * random.uniform(0.70, 1.30)
            elif prop_type == "rushing_yards":
                base_avg = 80
                game_value = base_avg * coach_factor * random.uniform(0.65, 1.35)
            elif prop_type == "receiving_yards":
                base_avg = 60
                game_value = base_avg * coach_factor * random.uniform(0.60, 1.40)
            else:
                base_avg = 50
                game_value = base_avg * coach_factor * random.uniform(0.75, 1.25)
            
            games.append({
                "game_date": f"202{random.randint(2, 4)}-{random.randint(9, 12):02d}-{random.randint(1, 28):02d}",
                "value": round(game_value, 1),
                "over_line": random.choice([True, False])
            })
            total_value += game_value
        
        avg_value = total_value / num_games if num_games > 0 else 0
        over_rate = sum(1 for g in games if g["over_line"]) / num_games if num_games > 0 else 0.5
        
        return {
            "player_name": player_name,
            "opponent_coach": opponent_coach,
            "prop_type": prop_type,
            "num_games": num_games,
            "average_value": round(avg_value, 1),
            "over_rate": round(over_rate, 3),
            "games": games,
            "coach_factor": round(coach_factor, 3),  # How this coach affects this player
            "trend": "improving" if games[-1]["value"] > avg_value else "declining" if len(games) > 1 else "stable"
        }
    
    def get_team_coach(
        self,
        team_name: str,
        sport: str = "nfl"
    ) -> str:
        """
        Get the defensive coordinator for a team (for player prop analysis)
        
        Args:
            team_name: Team name
            sport: Sport type
        
        Returns:
            Defensive coordinator name
        """
        # Mock coach assignments - in production, fetch from team data
        coach_map = {
            "Kansas City Chiefs": "Steve Spagnuolo",
            "Buffalo Bills": "Leslie Frazier",
            "Philadelphia Eagles": "Sean Desai",
            "Los Angeles Chargers": "Brandon Staley",
            "San Francisco 49ers": "DeMeco Ryans",
            "Seattle Seahawks": "Clint Hurtt",
            "Miami Dolphins": "Vic Fangio",
            "New York Jets": "Robert Saleh",
            "Baltimore Ravens": "Mike Macdonald",
            "Pittsburgh Steelers": "Teryl Austin",
            "Green Bay Packers": "Joe Barry",
            "Chicago Bears": "Alan Williams",
            "Detroit Lions": "Aaron Glenn",
            "Minnesota Vikings": "Ed Donatell",
            "Cleveland Browns": "Jim Schwartz",
            "Cincinnati Bengals": "Lou Anarumo",
            "Dallas Cowboys": "Dan Quinn",
            "New England Patriots": "Bill Belichick",
            "Tampa Bay Buccaneers": "Todd Bowles",
            "Atlanta Falcons": "Dean Pees",
            "Los Angeles Rams": "Raheem Morris",
            "Arizona Cardinals": "Vance Joseph",
            "Las Vegas Raiders": "Patrick Graham",
            "Denver Broncos": "Ejiro Evero",
            "Tennessee Titans": "Shane Bowen",
            "Jacksonville Jaguars": "Mike Caldwell",
            "New Orleans Saints": "Pete Werner",
            "Carolina Panthers": "Al Holcomb",
            "Indianapolis Colts": "Gus Bradley",
            "Houston Texans": "Lovie Smith",
            "Washington Commanders": "Jack Del Rio",
            "New York Giants": "Wink Martindale"
        }
        
        return coach_map.get(team_name, "Unknown Coach")
    
    def get_team_coach_for_sport(
        self,
        team_name: str,
        sport: str = "nfl"
    ) -> str:
        """
        Get the defensive coordinator or head coach for a team based on sport
        
        Args:
            team_name: Team name
            sport: Sport type (nfl, nba, mlb, nhl)
        
        Returns:
            Coach name
        """
        if sport == "nfl":
            return self.get_team_coach(team_name, sport)
        elif sport == "nba":
            # NBA head coaches
            nba_coaches = {
                "Los Angeles Lakers": "Darvin Ham",
                "Boston Celtics": "Joe Mazzulla",
                "Golden State Warriors": "Steve Kerr",
                "Milwaukee Bucks": "Doc Rivers",
                "Miami Heat": "Erik Spoelstra",
                "New York Knicks": "Tom Thibodeau",
                "Denver Nuggets": "Michael Malone",
                "Phoenix Suns": "Frank Vogel",
                "Dallas Mavericks": "Jason Kidd",
                "Chicago Bulls": "Billy Donovan",
            }
            return nba_coaches.get(team_name, "Unknown NBA Coach")
        elif sport == "mlb":
            # MLB managers
            mlb_managers = {
                "New York Yankees": "Aaron Boone",
                "Boston Red Sox": "Alex Cora",
                "Los Angeles Dodgers": "Dave Roberts",
                "San Francisco Giants": "Bob Melvin",
                "Chicago Cubs": "Craig Counsell",
                "St. Louis Cardinals": "Oliver Marmol",
                "Houston Astros": "Joe Espada",
                "Texas Rangers": "Bruce Bochy",
                "Atlanta Braves": "Brian Snitker",
                "Philadelphia Phillies": "Rob Thomson",
            }
            return mlb_managers.get(team_name, "Unknown MLB Manager")
        elif sport == "nhl":
            # NHL head coaches
            nhl_coaches = {
                "Toronto Maple Leafs": "Sheldon Keefe",
                "Boston Bruins": "Jim Montgomery",
                "Montreal Canadiens": "Martin St. Louis",
                "New York Rangers": "Peter Laviolette",
                "Edmonton Oilers": "Kris Knoblauch",
                "Vancouver Canucks": "Rick Tocchet",
                "Chicago Blackhawks": "Luke Richardson",
                "Detroit Red Wings": "Derek Lalonde",
                "Pittsburgh Penguins": "Mike Sullivan",
                "Washington Capitals": "Spencer Carbery",
            }
            return nhl_coaches.get(team_name, "Unknown NHL Coach")
        else:
            return "Unknown Coach"
    
    def get_head_coach(
        self,
        team_name: str,
        sport: str = "nfl"
    ) -> str:
        """
        Get the head coach for a team
        
        Args:
            team_name: Team name
            sport: Sport type
        
        Returns:
            Head coach name
        """
        # Mock head coach assignments - in production, fetch from team data
        head_coach_map = {
            "Kansas City Chiefs": "Andy Reid",
            "Buffalo Bills": "Sean McDermott",
            "Philadelphia Eagles": "Nick Sirianni",
            "Los Angeles Chargers": "Brandon Staley",
            "San Francisco 49ers": "Kyle Shanahan",
            "Seattle Seahawks": "Pete Carroll",
            "Miami Dolphins": "Mike McDaniel",
            "New York Jets": "Robert Saleh",
            "Baltimore Ravens": "John Harbaugh",
            "Pittsburgh Steelers": "Mike Tomlin",
            "Green Bay Packers": "Matt LaFleur",
            "Chicago Bears": "Matt Eberflus",
            "Detroit Lions": "Dan Campbell",
            "Minnesota Vikings": "Kevin O'Connell",
            "Cleveland Browns": "Kevin Stefanski",
            "Cincinnati Bengals": "Zac Taylor",
            "Dallas Cowboys": "Mike McCarthy",
            "New England Patriots": "Bill Belichick",
            "Tampa Bay Buccaneers": "Todd Bowles",
            "Atlanta Falcons": "Arthur Smith",
            "Los Angeles Rams": "Sean McVay",
            "Arizona Cardinals": "Jonathan Gannon",
            "Las Vegas Raiders": "Antonio Pierce",
            "Denver Broncos": "Sean Payton",
            "Tennessee Titans": "Mike Vrabel",
            "Jacksonville Jaguars": "Doug Pederson",
            "New Orleans Saints": "Dennis Allen",
            "Carolina Panthers": "Frank Reich",
            "Indianapolis Colts": "Shane Steichen",
            "Houston Texans": "DeMeco Ryans",
            "Washington Commanders": "Ron Rivera",
            "New York Giants": "Brian Daboll"
        }
        
        if sport == "nfl":
            return head_coach_map.get(team_name, "Unknown Head Coach")
        elif sport == "nba":
            nba_coaches = {
                "Los Angeles Lakers": "Darvin Ham",
                "Boston Celtics": "Joe Mazzulla",
                "Golden State Warriors": "Steve Kerr",
                "Milwaukee Bucks": "Doc Rivers",
                "Miami Heat": "Erik Spoelstra",
                "New York Knicks": "Tom Thibodeau",
                "Denver Nuggets": "Michael Malone",
                "Phoenix Suns": "Frank Vogel",
                "Dallas Mavericks": "Jason Kidd",
                "Chicago Bulls": "Billy Donovan",
            }
            return nba_coaches.get(team_name, "Unknown NBA Coach")
        elif sport == "mlb":
            mlb_managers = {
                "New York Yankees": "Aaron Boone",
                "Boston Red Sox": "Alex Cora",
                "Los Angeles Dodgers": "Dave Roberts",
                "San Francisco Giants": "Bob Melvin",
                "Chicago Cubs": "Craig Counsell",
                "St. Louis Cardinals": "Oliver Marmol",
                "Houston Astros": "Joe Espada",
                "Texas Rangers": "Bruce Bochy",
                "Atlanta Braves": "Brian Snitker",
                "Philadelphia Phillies": "Rob Thomson",
            }
            return mlb_managers.get(team_name, "Unknown MLB Manager")
        elif sport == "nhl":
            nhl_coaches = {
                "Toronto Maple Leafs": "Sheldon Keefe",
                "Boston Bruins": "Jim Montgomery",
                "Montreal Canadiens": "Martin St. Louis",
                "New York Rangers": "Peter Laviolette",
                "Edmonton Oilers": "Kris Knoblauch",
                "Vancouver Canucks": "Rick Tocchet",
                "Chicago Blackhawks": "Luke Richardson",
                "Detroit Red Wings": "Derek Lalonde",
                "Pittsburgh Penguins": "Mike Sullivan",
                "Washington Capitals": "Spencer Carbery",
            }
            return nhl_coaches.get(team_name, "Unknown NHL Coach")
        else:
            return head_coach_map.get(team_name, "Unknown Head Coach")
    
    def get_coach_vs_coach_history(
        self,
        home_coach: str,
        away_coach: str,
        sport: str = "nfl"
    ) -> Dict:
        """
        Get historical head-to-head record between two head coaches
        
        Args:
            home_coach: Home team head coach
            away_coach: Away team head coach
            sport: Sport type
        
        Returns:
            Dictionary with historical matchup statistics
        """
        # Create deterministic seed based on coach names
        seed = hash(f"{home_coach}_{away_coach}") % 1000
        random.seed(seed)
        
        # Simulate historical matchups between these coaches
        # Some coaches have better records against certain other coaches
        num_games = random.randint(2, 8)  # Coaches may have faced each other 2-8 times
        
        home_wins = 0
        away_wins = 0
        games = []
        
        # Determine if one coach has an advantage (based on coaching style, schemes, etc.)
        # This creates realistic patterns where some coaches match up better
        home_advantage_factor = random.uniform(0.40, 0.60)  # Home coach win rate
        
        for i in range(num_games):
            # Simulate game outcome
            if random.random() < home_advantage_factor:
                home_wins += 1
                winner = "home"
            else:
                away_wins += 1
                winner = "away"
            
            games.append({
                "game_date": f"202{random.randint(0, 4)}-{random.randint(9, 12):02d}-{random.randint(1, 28):02d}",
                "home_score": random.randint(17, 35),
                "away_score": random.randint(17, 35),
                "winner": winner
            })
        
        home_win_rate = home_wins / num_games if num_games > 0 else 0.5
        away_win_rate = away_wins / num_games if num_games > 0 else 0.5
        
        # Calculate average point differential
        point_differentials = []
        for game in games:
            if game["winner"] == "home":
                point_diff = game["home_score"] - game["away_score"]
            else:
                point_diff = game["away_score"] - game["home_score"]
            point_differentials.append(point_diff)
        
        avg_point_diff = sum(point_differentials) / len(point_differentials) if point_differentials else 0
        
        # Determine if there's a coaching advantage
        if home_win_rate > 0.60:
            advantage = "home_coach"
            advantage_strength = "strong" if home_win_rate > 0.70 else "moderate"
        elif away_win_rate > 0.60:
            advantage = "away_coach"
            advantage_strength = "strong" if away_win_rate > 0.70 else "moderate"
        else:
            advantage = "neutral"
            advantage_strength = "none"
        
        # Calculate win streak
        win_streak = 0
        if len(games) > 0:
            last_winner = games[-1]["winner"]
            for game in reversed(games):
                if game["winner"] == last_winner:
                    win_streak += 1
                else:
                    break
        
        # Format win/loss record as "W-L" (e.g., "5-3")
        home_record = f"{home_wins}-{away_wins}"
        away_record = f"{away_wins}-{home_wins}"
        
        return {
            "home_coach": home_coach,
            "away_coach": away_coach,
            "num_games": num_games,
            "home_coach_wins": home_wins,
            "away_coach_wins": away_wins,
            "home_coach_record": home_record,  # Format: "W-L"
            "away_coach_record": away_record,  # Format: "W-L"
            "home_coach_win_rate": round(home_win_rate, 3),
            "away_coach_win_rate": round(away_win_rate, 3),
            "avg_point_differential": round(avg_point_diff, 1),
            "advantage": advantage,
            "advantage_strength": advantage_strength,
            "games": games,
            "recent_trend": "home_coach" if games[-1]["winner"] == "home" else "away_coach" if len(games) > 0 else "neutral",
            "current_streak": {
                "coach": last_winner if len(games) > 0 else None,
                "length": win_streak,
                "description": f"{home_coach if last_winner == 'home' else away_coach} has won {win_streak} in a row" if win_streak > 1 and len(games) > 0 else None
            }
        }
    
    def calculate_matchup_adjustment(
        self,
        player_name: str,
        opponent_team: str,
        opponent_coach: str,
        prop_type: str,
        base_prediction: float,
        sport: str = "nfl"
    ) -> Dict:
        """
        Calculate how historical matchups should adjust the base prediction
        
        Args:
            player_name: Player name
            opponent_team: Opponent team
            opponent_coach: Opponent coach
            prop_type: Prop type
            base_prediction: Base prediction value
            sport: Sport type
        
        Returns:
            Dictionary with adjusted prediction and factors
        """
        # Get historical data
        team_history = self.get_player_vs_team_history(
            player_name, opponent_team, prop_type, sport
        )
        coach_history = self.get_player_vs_coach_history(
            player_name, opponent_coach, prop_type, sport
        )
        
        # Calculate adjustments
        # Weight team history more (60%) than coach history (40%)
        # since team matchups are more frequent
        team_adjustment = (team_history["matchup_factor"] - 1.0) * 0.6
        coach_adjustment = (coach_history["coach_factor"] - 1.0) * 0.4
        
        total_adjustment = team_adjustment + coach_adjustment
        
        # Apply adjustment to base prediction
        adjusted_prediction = base_prediction * (1.0 + total_adjustment)
        
        # Calculate confidence boost from having historical data
        confidence_boost = min(0.15, (team_history["num_games"] + coach_history["num_games"]) * 0.02)
        
        return {
            "base_prediction": round(base_prediction, 1),
            "adjusted_prediction": round(adjusted_prediction, 1),
            "team_matchup_factor": team_history["matchup_factor"],
            "coach_matchup_factor": coach_history["coach_factor"],
            "total_adjustment": round(total_adjustment, 3),
            "team_history_avg": team_history["average_value"],
            "coach_history_avg": coach_history["average_value"],
            "team_over_rate": team_history["over_rate"],
            "coach_over_rate": coach_history["over_rate"],
            "confidence_boost": round(confidence_boost, 3),
            "historical_games": team_history["num_games"] + coach_history["num_games"]
        }
    
    def analyze_coaching_matchup(
        self,
        home_team: str,
        away_team: str,
        sport: str = "nfl"
    ) -> Dict:
        """
        Analyze the head coach vs head coach matchup
        
        Args:
            home_team: Home team name
            away_team: Away team name
            sport: Sport type
        
        Returns:
            Dictionary with coaching matchup analysis and adjustment factor
        """
        home_coach = self.get_head_coach(home_team, sport)
        away_coach = self.get_head_coach(away_team, sport)
        
        # Get historical matchup
        coach_history = self.get_coach_vs_coach_history(home_coach, away_coach, sport)
        
        # Calculate adjustment factor for game prediction
        # If home coach has advantage, boost home team probability
        # If away coach has advantage, reduce home team probability
        adjustment = 0.0
        
        if coach_history["advantage"] == "home_coach":
            if coach_history["advantage_strength"] == "strong":
                adjustment = 0.05  # 5% boost for strong advantage
            else:
                adjustment = 0.03  # 3% boost for moderate advantage
        elif coach_history["advantage"] == "away_coach":
            if coach_history["advantage_strength"] == "strong":
                adjustment = -0.05  # 5% reduction for strong advantage
            else:
                adjustment = -0.03  # 3% reduction for moderate advantage
        
        # Factor in point differential (larger margins = stronger advantage)
        if abs(coach_history["avg_point_differential"]) > 7:
            adjustment *= 1.2  # Boost adjustment if large point differentials
        elif abs(coach_history["avg_point_differential"]) < 3:
            adjustment *= 0.8  # Reduce adjustment if close games
        
        # Cap adjustment
        adjustment = max(-0.08, min(0.08, adjustment))
        
        return {
            "home_coach": home_coach,
            "away_coach": away_coach,
            "home_team": home_team,  # Include team names
            "away_team": away_team,  # Include team names
            "historical_record": coach_history,
            "adjustment_factor": round(adjustment, 3),
            "key_insight": self._generate_coaching_insight(coach_history, home_team, away_team)
        }
    
    def _generate_coaching_insight(self, coach_history: Dict, home_team: str = "", away_team: str = "") -> str:
        """Generate a human-readable insight about the coaching matchup"""
        if coach_history["num_games"] == 0:
            return "No previous head-to-head coaching history"
        
        home_record = coach_history.get("home_coach_record", f"{coach_history['home_coach_wins']}-{coach_history['away_coach_wins']}")
        away_record = coach_history.get("away_coach_record", f"{coach_history['away_coach_wins']}-{coach_history['home_coach_wins']}")
        
        # Include team names in coach references
        home_coach_display = f"{coach_history['home_coach']} ({home_team})" if home_team else coach_history['home_coach']
        away_coach_display = f"{coach_history['away_coach']} ({away_team})" if away_team else coach_history['away_coach']
        
        # Include win/loss record in the insight
        record_info = f" ({home_record} vs {away_record})"
        
        if coach_history["advantage"] == "home_coach":
            if coach_history["advantage_strength"] == "strong":
                return f"{home_coach_display} has a strong historical advantage{record_info} - {coach_history['home_coach_win_rate']:.0%} win rate in {coach_history['num_games']} games"
            else:
                return f"{home_coach_display} has a moderate advantage{record_info} - {coach_history['home_coach_win_rate']:.0%} win rate in {coach_history['num_games']} games"
        elif coach_history["advantage"] == "away_coach":
            if coach_history["advantage_strength"] == "strong":
                return f"{away_coach_display} has a strong historical advantage{record_info} - {coach_history['away_coach_win_rate']:.0%} win rate in {coach_history['num_games']} games"
            else:
                return f"{away_coach_display} has a moderate advantage{record_info} - {coach_history['away_coach_win_rate']:.0%} win rate in {coach_history['num_games']} games"
        else:
            return f"Coaching matchup is historically even{record_info} - {coach_history['home_coach_win_rate']:.0%} vs {coach_history['away_coach_win_rate']:.0%} in {coach_history['num_games']} games"

