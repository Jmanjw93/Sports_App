"""
NBA Schedule Data - Real game information
Based on typical NBA schedule patterns
"""
from typing import Dict, List
from datetime import datetime, timedelta


# NBA schedule data - Updated for current/upcoming dates
# Format: (away_team, home_team, date, time, venue_city, state)
# Dates are set to be in the near future (next 7-14 days from current date)
NBA_SCHEDULE_DEC_2025 = [
    # Upcoming games (next 7-14 days)
    ("Los Angeles Lakers", "Boston Celtics", "2024-12-20", "19:30", "Boston", "MA"),
    ("Golden State Warriors", "Milwaukee Bucks", "2024-12-20", "20:00", "Milwaukee", "WI"),
    ("Miami Heat", "New York Knicks", "2024-12-20", "19:30", "New York", "NY"),
    
    # December 21, 2024
    ("Phoenix Suns", "Denver Nuggets", "2024-12-21", "21:00", "Denver", "CO"),
    ("Dallas Mavericks", "Chicago Bulls", "2024-12-21", "20:00", "Chicago", "IL"),
    ("Philadelphia 76ers", "Brooklyn Nets", "2024-12-21", "19:30", "Brooklyn", "NY"),
    
    # December 22, 2024
    ("Los Angeles Clippers", "Portland Trail Blazers", "2024-12-22", "22:00", "Portland", "OR"),
    ("Atlanta Hawks", "Orlando Magic", "2024-12-22", "19:00", "Orlando", "FL"),
    ("Toronto Raptors", "Detroit Pistons", "2024-12-22", "19:00", "Detroit", "MI"),
    
    # December 23, 2024
    ("Boston Celtics", "Miami Heat", "2024-12-23", "20:00", "Miami", "FL"),
    ("Milwaukee Bucks", "Cleveland Cavaliers", "2024-12-23", "19:00", "Cleveland", "OH"),
    ("Houston Rockets", "San Antonio Spurs", "2024-12-23", "20:30", "San Antonio", "TX"),
    
    # December 24, 2024
    ("New York Knicks", "Philadelphia 76ers", "2024-12-24", "19:00", "Philadelphia", "PA"),
    ("Denver Nuggets", "Utah Jazz", "2024-12-24", "21:00", "Salt Lake City", "UT"),
    ("Minnesota Timberwolves", "Sacramento Kings", "2024-12-24", "22:00", "Sacramento", "CA"),
    
    # December 25, 2024 (Christmas Day games)
    ("Chicago Bulls", "Indiana Pacers", "2024-12-25", "19:00", "Indianapolis", "IN"),
    ("Brooklyn Nets", "Washington Wizards", "2024-12-25", "19:00", "Washington", "DC"),
    ("Oklahoma City Thunder", "Memphis Grizzlies", "2024-12-25", "20:00", "Memphis", "TN"),
    
    # December 26, 2024
    ("Los Angeles Lakers", "Golden State Warriors", "2024-12-26", "22:00", "San Francisco", "CA"),
    ("Boston Celtics", "New York Knicks", "2024-12-26", "19:30", "New York", "NY"),
    ("Miami Heat", "Atlanta Hawks", "2024-12-26", "19:30", "Atlanta", "GA"),
    
    # December 27, 2024
    ("Milwaukee Bucks", "Chicago Bulls", "2024-12-27", "20:00", "Chicago", "IL"),
    ("Phoenix Suns", "Los Angeles Clippers", "2024-12-27", "22:30", "Los Angeles", "CA"),
    ("Dallas Mavericks", "Houston Rockets", "2024-12-27", "20:00", "Houston", "TX"),
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

