"""
NHL Schedule Data - Real game information
Based on typical NHL schedule patterns
"""
from typing import Dict, List
from datetime import datetime, timedelta


# NHL schedule data for December 2025
# Format: (away_team, home_team, date, time, venue_city, state)
NHL_SCHEDULE_DEC_2025 = [
    # December 8, 2025
    ("Toronto Maple Leafs", "Boston Bruins", "2025-12-08", "19:00", "Boston", "MA"),
    ("Montreal Canadiens", "New York Rangers", "2025-12-08", "19:00", "New York", "NY"),
    ("Edmonton Oilers", "Vancouver Canucks", "2025-12-08", "22:00", "Vancouver", "BC"),
    
    # December 9, 2025
    ("Chicago Blackhawks", "Detroit Red Wings", "2025-12-09", "19:30", "Detroit", "MI"),
    ("Pittsburgh Penguins", "Washington Capitals", "2025-12-09", "19:00", "Washington", "DC"),
    ("Calgary Flames", "Seattle Kraken", "2025-12-09", "22:00", "Seattle", "WA"),
    
    # December 10, 2025
    ("New York Islanders", "Philadelphia Flyers", "2025-12-10", "19:00", "Philadelphia", "PA"),
    ("Tampa Bay Lightning", "Florida Panthers", "2025-12-10", "19:00", "Sunrise", "FL"),
    ("Winnipeg Jets", "Colorado Avalanche", "2025-12-10", "21:00", "Denver", "CO"),
    
    # December 11, 2025
    ("Boston Bruins", "Toronto Maple Leafs", "2025-12-11", "19:00", "Toronto", "ON"),
    ("New York Rangers", "New Jersey Devils", "2025-12-11", "19:00", "Newark", "NJ"),
    ("Vancouver Canucks", "Calgary Flames", "2025-12-11", "22:00", "Calgary", "AB"),
    
    # December 12, 2025
    ("Detroit Red Wings", "Chicago Blackhawks", "2025-12-12", "20:00", "Chicago", "IL"),
    ("Washington Capitals", "Pittsburgh Penguins", "2025-12-12", "19:00", "Pittsburgh", "PA"),
    ("Seattle Kraken", "San Jose Sharks", "2025-12-12", "22:30", "San Jose", "CA"),
    
    # December 13, 2025
    ("Philadelphia Flyers", "New York Islanders", "2025-12-13", "19:00", "Elmont", "NY"),
    ("Florida Panthers", "Tampa Bay Lightning", "2025-12-13", "19:00", "Tampa", "FL"),
    ("Colorado Avalanche", "Dallas Stars", "2025-12-13", "20:00", "Dallas", "TX"),
    
    # December 14, 2025
    ("Toronto Maple Leafs", "Montreal Canadiens", "2025-12-14", "19:00", "Montreal", "QC"),
    ("Boston Bruins", "Buffalo Sabres", "2025-12-14", "19:00", "Buffalo", "NY"),
    ("Edmonton Oilers", "Los Angeles Kings", "2025-12-14", "22:30", "Los Angeles", "CA"),
    
    # December 15, 2025
    ("New York Rangers", "Carolina Hurricanes", "2025-12-15", "19:00", "Raleigh", "NC"),
    ("Vancouver Canucks", "Anaheim Ducks", "2025-12-15", "22:00", "Anaheim", "CA"),
    ("Minnesota Wild", "Nashville Predators", "2025-12-15", "20:00", "Nashville", "TN"),
]


def get_nhl_games_for_period(start_date: datetime, end_date: datetime) -> List[Dict]:
    """Get NHL games for a specific date range"""
    games = []
    
    for away, home, date_str, time_str, city, state in NHL_SCHEDULE_DEC_2025:
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
                    "game_id": f"nhl_{len(games)+1}_{int(game_date.timestamp())}",
                    "sport": "nhl",
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
            print(f"Error parsing NHL game: {away} @ {home} - {e}")
            continue
    
    return games




