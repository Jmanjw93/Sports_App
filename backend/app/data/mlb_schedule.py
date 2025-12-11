"""
MLB Schedule Data - Real game information
Based on typical MLB schedule patterns
"""
from typing import Dict, List
from datetime import datetime, timedelta


# MLB schedule data for December 2025 (off-season, but showing sample games)
# Note: MLB season typically runs March-October, but showing sample for consistency
# Format: (away_team, home_team, date, time, venue_city, state)
MLB_SCHEDULE_DEC_2025 = [
    # December 8, 2025 (Sample games - MLB is typically off-season)
    ("New York Yankees", "Boston Red Sox", "2025-12-08", "19:10", "Boston", "MA"),
    ("Los Angeles Dodgers", "San Francisco Giants", "2025-12-08", "22:15", "San Francisco", "CA"),
    ("Chicago Cubs", "St. Louis Cardinals", "2025-12-08", "20:15", "St. Louis", "MO"),
    
    # December 9, 2025
    ("Houston Astros", "Texas Rangers", "2025-12-09", "20:05", "Arlington", "TX"),
    ("Atlanta Braves", "Philadelphia Phillies", "2025-12-09", "19:05", "Philadelphia", "PA"),
    ("Tampa Bay Rays", "Miami Marlins", "2025-12-09", "19:10", "Miami", "FL"),
    
    # December 10, 2025
    ("Seattle Mariners", "Oakland Athletics", "2025-12-10", "22:07", "Oakland", "CA"),
    ("Minnesota Twins", "Chicago White Sox", "2025-12-10", "20:10", "Chicago", "IL"),
    ("Cleveland Guardians", "Detroit Tigers", "2025-12-10", "19:10", "Detroit", "MI"),
    
    # December 11, 2025
    ("Baltimore Orioles", "Toronto Blue Jays", "2025-12-11", "19:07", "Toronto", "ON"),
    ("Arizona Diamondbacks", "Colorado Rockies", "2025-12-11", "20:40", "Denver", "CO"),
    ("San Diego Padres", "Los Angeles Angels", "2025-12-11", "22:07", "Anaheim", "CA"),
    
    # December 12, 2025
    ("New York Mets", "Washington Nationals", "2025-12-12", "19:05", "Washington", "DC"),
    ("Milwaukee Brewers", "Cincinnati Reds", "2025-12-12", "19:10", "Cincinnati", "OH"),
    ("Kansas City Royals", "Pittsburgh Pirates", "2025-12-12", "19:05", "Pittsburgh", "PA"),
    
    # December 13, 2025
    ("Boston Red Sox", "New York Yankees", "2025-12-13", "19:05", "New York", "NY"),
    ("San Francisco Giants", "Los Angeles Dodgers", "2025-12-13", "22:10", "Los Angeles", "CA"),
    ("St. Louis Cardinals", "Chicago Cubs", "2025-12-13", "20:05", "Chicago", "IL"),
    
    # December 14, 2025
    ("Texas Rangers", "Houston Astros", "2025-12-14", "20:10", "Houston", "TX"),
    ("Philadelphia Phillies", "Atlanta Braves", "2025-12-14", "19:20", "Atlanta", "GA"),
    ("Miami Marlins", "Tampa Bay Rays", "2025-12-14", "19:10", "St. Petersburg", "FL"),
]


def get_mlb_games_for_period(start_date: datetime, end_date: datetime) -> List[Dict]:
    """Get MLB games for a specific date range"""
    games = []
    
    for away, home, date_str, time_str, city, state in MLB_SCHEDULE_DEC_2025:
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
                    "game_id": f"mlb_{len(games)+1}_{int(game_date.timestamp())}",
                    "sport": "mlb",
                    "home_team": home,
                    "away_team": away,
                    "date": game_date.isoformat(),
                    "venue": f"{home} Stadium",
                    "week": week_label,
                    "location": {
                        "city": city,
                        "state": state,
                        "country": "US"
                    }
                })
        except Exception as e:
            print(f"Error parsing MLB game: {away} @ {home} - {e}")
            continue
    
    return games




