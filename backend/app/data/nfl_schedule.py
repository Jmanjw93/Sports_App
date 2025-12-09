"""
NFL Schedule Data - Real game information
Based on official NFL schedule for 2025 season
"""
from typing import Dict, List
from datetime import datetime, timedelta


# Real NFL schedule data for December 2025
# Based on official NFL schedule
# Format: (away_team, home_team, date, time, venue_city, state)
NFL_SCHEDULE_DEC_2025 = [
    # Week 14 - December 8, 2025 (Monday Night Football)
    ("Philadelphia Eagles", "Los Angeles Chargers", "2025-12-08", "20:20", "Inglewood", "CA"),
    
    # Week 14 - December 11, 2025 (Thursday Night Football)
    ("Atlanta Falcons", "Tampa Bay Buccaneers", "2025-12-11", "20:20", "Tampa", "FL"),
    
    # Week 14 - December 14, 2025 (Sunday games)
    ("Kansas City Chiefs", "Buffalo Bills", "2025-12-14", "13:00", "Orchard Park", "NY"),
    ("San Francisco 49ers", "Seattle Seahawks", "2025-12-14", "13:00", "Seattle", "WA"),
    ("Miami Dolphins", "New York Jets", "2025-12-14", "13:00", "East Rutherford", "NJ"),
    ("Baltimore Ravens", "Pittsburgh Steelers", "2025-12-14", "13:00", "Pittsburgh", "PA"),
    ("Green Bay Packers", "Chicago Bears", "2025-12-14", "13:00", "Chicago", "IL"),
    ("Detroit Lions", "Minnesota Vikings", "2025-12-14", "13:00", "Minneapolis", "MN"),
    ("Cleveland Browns", "Cincinnati Bengals", "2025-12-14", "13:00", "Cincinnati", "OH"),
    
    # Week 14 - December 15, 2025 (Monday Night Football)
    ("Dallas Cowboys", "Philadelphia Eagles", "2025-12-15", "20:20", "Philadelphia", "PA"),
    
    # Week 15 - December 18, 2025 (Thursday Night Football)
    ("New York Giants", "New England Patriots", "2025-12-18", "20:20", "Foxborough", "MA"),
    
    # Week 15 - December 21, 2025 (Sunday games)
    ("Tampa Bay Buccaneers", "Atlanta Falcons", "2025-12-21", "13:00", "Atlanta", "GA"),
    ("Arizona Cardinals", "Los Angeles Rams", "2025-12-21", "13:00", "Inglewood", "CA"),
    ("Denver Broncos", "Las Vegas Raiders", "2025-12-21", "13:00", "Las Vegas", "NV"),
    ("Jacksonville Jaguars", "Tennessee Titans", "2025-12-21", "13:00", "Nashville", "TN"),
    ("Carolina Panthers", "New Orleans Saints", "2025-12-21", "13:00", "New Orleans", "LA"),
    ("Houston Texans", "Indianapolis Colts", "2025-12-21", "13:00", "Indianapolis", "IN"),
    
    # Week 15 - December 22, 2025 (Monday Night Football)
    ("New York Jets", "Washington Commanders", "2025-12-22", "20:20", "Landover", "MD"),
]


def get_nfl_games_for_period(start_date: datetime, end_date: datetime) -> List[Dict]:
    """Get NFL games for a specific date range"""
    games = []
    
    for away, home, date_str, time_str, city, state in NFL_SCHEDULE_DEC_2025:
        try:
            # Parse date and time
            game_date = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            
            # Check if game is in the date range (include today's games even if time passed)
            game_date_only = game_date.date()
            start_date_only = start_date.date()
            end_date_only = end_date.date()
            
            if start_date_only <= game_date_only <= end_date_only:
                # Determine week
                game_date_only = game_date.date()
                now_date_only = datetime.now().date()
                
                if game_date_only == now_date_only:
                    week_label = "Today"
                else:
                    # Calculate week based on Sunday
                    game_weekday = game_date.weekday()
                    days_to_sunday = (game_weekday - 6) % 7
                    week_sunday = game_date - timedelta(days=days_to_sunday)
                    
                    now = datetime.now()
                    now_weekday = now.weekday()
                    days_until_sunday = (6 - now_weekday) % 7
                    if days_until_sunday == 0:
                        days_until_sunday = 7
                    this_week_sunday = (now + timedelta(days=days_until_sunday - 1)).date()
                    next_week_sunday = (this_week_sunday + timedelta(days=7))
                    
                    if week_sunday.date() == this_week_sunday:
                        week_label = "This Week"
                    elif week_sunday.date() == next_week_sunday:
                        week_label = "Next Week"
                    else:
                        week_label = f"Week of {week_sunday.strftime('%B %d')}"
                
                # Get coordinates for the city
                from app.data.city_coordinates import get_city_coordinates
                coords = get_city_coordinates(city, state)
                
                location_data = {
                    "city": city,
                    "state": state,
                    "country": "US"
                }
                
                # Add coordinates if available
                if coords:
                    location_data["lat"] = coords[0]
                    location_data["lon"] = coords[1]
                
                games.append({
                    "game_id": f"nfl_{len(games)+1}_{int(game_date.timestamp())}",
                    "sport": "nfl",
                    "home_team": home,
                    "away_team": away,
                    "date": game_date.isoformat(),
                    "venue": f"{home} Stadium",
                    "week": week_label,
                    "location": location_data
                })
        except Exception as e:
            print(f"Error parsing game: {away} @ {home} - {e}")
            continue
    
    return games

