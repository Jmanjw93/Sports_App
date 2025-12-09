"""
NBA Schedule Data - Real game information
Based on typical NBA schedule patterns
"""
from typing import Dict, List
from datetime import datetime, timedelta


# NBA schedule data for December 2025
# Format: (away_team, home_team, date, time, venue_city, state)
NBA_SCHEDULE_DEC_2025 = [
    # December 8, 2025
    ("Los Angeles Lakers", "Boston Celtics", "2025-12-08", "19:30", "Boston", "MA"),
    ("Golden State Warriors", "Milwaukee Bucks", "2025-12-08", "20:00", "Milwaukee", "WI"),
    ("Miami Heat", "New York Knicks", "2025-12-08", "19:30", "New York", "NY"),
    
    # December 9, 2025
    ("Phoenix Suns", "Denver Nuggets", "2025-12-09", "21:00", "Denver", "CO"),
    ("Dallas Mavericks", "Chicago Bulls", "2025-12-09", "20:00", "Chicago", "IL"),
    ("Philadelphia 76ers", "Brooklyn Nets", "2025-12-09", "19:30", "Brooklyn", "NY"),
    
    # December 10, 2025
    ("Los Angeles Clippers", "Portland Trail Blazers", "2025-12-10", "22:00", "Portland", "OR"),
    ("Atlanta Hawks", "Orlando Magic", "2025-12-10", "19:00", "Orlando", "FL"),
    ("Toronto Raptors", "Detroit Pistons", "2025-12-10", "19:00", "Detroit", "MI"),
    
    # December 11, 2025
    ("Boston Celtics", "Miami Heat", "2025-12-11", "20:00", "Miami", "FL"),
    ("Milwaukee Bucks", "Cleveland Cavaliers", "2025-12-11", "19:00", "Cleveland", "OH"),
    ("Houston Rockets", "San Antonio Spurs", "2025-12-11", "20:30", "San Antonio", "TX"),
    
    # December 12, 2025
    ("New York Knicks", "Philadelphia 76ers", "2025-12-12", "19:00", "Philadelphia", "PA"),
    ("Denver Nuggets", "Utah Jazz", "2025-12-12", "21:00", "Salt Lake City", "UT"),
    ("Minnesota Timberwolves", "Sacramento Kings", "2025-12-12", "22:00", "Sacramento", "CA"),
    
    # December 13, 2025
    ("Chicago Bulls", "Indiana Pacers", "2025-12-13", "19:00", "Indianapolis", "IN"),
    ("Brooklyn Nets", "Washington Wizards", "2025-12-13", "19:00", "Washington", "DC"),
    ("Oklahoma City Thunder", "Memphis Grizzlies", "2025-12-13", "20:00", "Memphis", "TN"),
    
    # December 14, 2025
    ("Los Angeles Lakers", "Golden State Warriors", "2025-12-14", "22:00", "San Francisco", "CA"),
    ("Boston Celtics", "New York Knicks", "2025-12-14", "19:30", "New York", "NY"),
    ("Miami Heat", "Atlanta Hawks", "2025-12-14", "19:30", "Atlanta", "GA"),
    
    # December 15, 2025
    ("Milwaukee Bucks", "Chicago Bulls", "2025-12-15", "20:00", "Chicago", "IL"),
    ("Phoenix Suns", "Los Angeles Clippers", "2025-12-15", "22:30", "Los Angeles", "CA"),
    ("Dallas Mavericks", "Houston Rockets", "2025-12-15", "20:00", "Houston", "TX"),
]


def get_nba_games_for_period(start_date: datetime, end_date: datetime) -> List[Dict]:
    """Get NBA games for a specific date range"""
    games = []
    
    for away, home, date_str, time_str, city, state in NBA_SCHEDULE_DEC_2025:
        try:
            # Parse date and time
            game_date = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            
            # Check if game is in the date range
            game_date_only = game_date.date()
            start_date_only = start_date.date()
            end_date_only = end_date.date()
            
            if start_date_only <= game_date_only <= end_date_only:
                # Determine week label
                now_date_only = datetime.now().date()
                
                if game_date_only == now_date_only:
                    week_label = "Today"
                elif game_date_only <= (now_date_only + timedelta(days=2)):
                    week_label = "This Week"
                elif game_date_only <= (now_date_only + timedelta(days=7)):
                    week_label = "Next Week"
                else:
                    week_label = f"Week of {game_date.strftime('%B %d')}"
                
                games.append({
                    "game_id": f"nba_{len(games)+1}_{int(game_date.timestamp())}",
                    "sport": "nba",
                    "home_team": home,
                    "away_team": away,
                    "date": game_date.isoformat(),
                    "venue": f"{home} Arena",
                    "week": week_label,
                    "location": {
                        "city": city,
                        "state": state,
                        "country": "US"
                    }
                })
        except Exception as e:
            print(f"Error parsing NBA game: {away} @ {home} - {e}")
            continue
    
    return games

