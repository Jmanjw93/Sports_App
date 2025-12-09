"""
City coordinates for accurate weather lookup
"""
from typing import Dict, Optional, Tuple

# Major US cities with their coordinates (lat, lon)
CITY_COORDINATES: Dict[str, Tuple[float, float]] = {
    # NFL Cities
    "Orchard Park": (42.7678, -78.7870),  # Buffalo Bills
    "Seattle": (47.6062, -122.3321),
    "East Rutherford": (40.8135, -74.0744),  # New York Jets
    "Pittsburgh": (40.4406, -79.9959),
    "Chicago": (41.8781, -87.6298),
    "Minneapolis": (44.9778, -93.2650),
    "Cincinnati": (39.1031, -84.5120),
    "Philadelphia": (39.9526, -75.1652),
    "Foxborough": (42.0654, -71.2478),  # New England Patriots
    "Atlanta": (33.7490, -84.3880),
    "Inglewood": (33.9617, -118.3531),  # LA Chargers/Rams
    "Las Vegas": (36.1699, -115.1398),
    "Nashville": (36.1627, -86.7816),
    "New Orleans": (29.9511, -90.0715),
    "Indianapolis": (39.7684, -86.1581),
    "Landover": (38.9072, -76.8650),  # Washington Commanders
    "Tampa": (27.9506, -82.4572),
    "Kansas City": (39.0997, -94.5786),
    "Miami": (25.7617, -80.1918),
    "Baltimore": (39.2904, -76.6122),
    "Green Bay": (44.5133, -88.0133),
    "Detroit": (42.3314, -83.0458),
    "Cleveland": (41.4993, -81.6944),
    "Dallas": (32.7767, -96.7970),
    "Denver": (39.7392, -104.9903),
    "Jacksonville": (30.3322, -81.6557),
    "Carolina": (35.2271, -80.8431),  # Charlotte
    "Houston": (29.7604, -95.3698),
    "Phoenix": (33.4484, -112.0740),
    "Oakland": (37.8044, -122.2712),
    "Santa Clara": (37.3541, -121.9552),  # San Francisco 49ers
    "Arlington": (32.7357, -97.1081),  # Dallas Cowboys
    "Glendale": (33.5387, -112.1860),  # Arizona Cardinals
    "Charlotte": (35.2271, -80.8431),  # Carolina Panthers
    
    # NBA Cities
    "Los Angeles": (34.0522, -118.2437),
    "Boston": (42.3601, -71.0589),
    "Golden State": (37.7749, -122.4194),  # San Francisco/Oakland
    "Milwaukee": (43.0389, -87.9065),
    "New York": (40.7128, -74.0060),
    "Denver": (39.7392, -104.9903),
    "Phoenix": (33.4484, -112.0740),
    
    # MLB Cities
    "Bronx": (40.8448, -73.8648),  # New York Yankees
    "St. Louis": (38.6270, -90.1994),
    "San Francisco": (37.7749, -122.4194),
    
    # NHL Cities
    "Toronto": (43.6532, -79.3832),
    "Montreal": (45.5017, -73.5673),
    "Edmonton": (53.5461, -113.4938),
    "Vancouver": (49.2827, -123.1207),
    "Detroit": (42.3314, -83.0458),
    "Washington": (38.9072, -76.8650),
}


def get_city_coordinates(city: str, state: Optional[str] = None) -> Optional[Tuple[float, float]]:
    """
    Get coordinates for a city
    
    Args:
        city: City name
        state: State abbreviation (optional)
    
    Returns:
        Tuple of (latitude, longitude) or None if not found
    """
    # Try exact city match first
    if city in CITY_COORDINATES:
        return CITY_COORDINATES[city]
    
    # Try case-insensitive match
    city_lower = city.lower()
    for key, coords in CITY_COORDINATES.items():
        if key.lower() == city_lower:
            return coords
    
    # Try partial match (e.g., "New York" matches "New York")
    for key, coords in CITY_COORDINATES.items():
        if city_lower in key.lower() or key.lower() in city_lower:
            return coords
    
    return None

