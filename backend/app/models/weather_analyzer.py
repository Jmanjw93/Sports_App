"""
Weather data collection and analysis
"""
from typing import Dict, Optional
from datetime import datetime
import requests
from app.config import settings


class WeatherAnalyzer:
    """Handles weather data collection and analysis"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.WEATHER_API_KEY
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    def get_weather_for_location(
        self,
        city: str,
        state: Optional[str] = None,
        country: str = "US"
    ) -> Optional[Dict]:
        """
        Get current weather for a location
        
        Args:
            city: City name
            state: State/Province (optional)
            country: Country code
        
        Returns:
            Dictionary with weather data or None if error
        """
        if not self.api_key:
            # Return mock data for development
            location_str = f"{city}, {state}" if state else city
            return self._get_mock_weather(location_str)
        
        try:
            location = f"{city},{state},{country}" if state else f"{city},{country}"
            url = f"{self.base_url}/weather"
            params = {
                "q": location,
                "appid": self.api_key,
                "units": "imperial"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "temp": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"].get("speed", 0),
                "wind_direction": data["wind"].get("deg", 0),
                "precipitation": data.get("rain", {}).get("1h", 0) or 
                               data.get("snow", {}).get("1h", 0),
                "conditions": data["weather"][0]["main"].lower(),
                "description": data["weather"][0]["description"],
                "visibility": data.get("visibility", 10000) / 1000,  # Convert to km
                "pressure": data["main"]["pressure"],
                "location": f"{city}, {state}" if state else city
            }
        except Exception as e:
            print(f"Error fetching weather: {e}")
            return self._get_mock_weather()
    
    def get_weather_for_coordinates(
        self,
        lat: float,
        lon: float
    ) -> Optional[Dict]:
        """
        Get weather for specific coordinates
        
        Args:
            lat: Latitude
            lon: Longitude
        
        Returns:
            Dictionary with weather data
        """
        if not self.api_key:
            location_str = f"({lat}, {lon})"
            return self._get_mock_weather(location_str)
        
        try:
            url = f"{self.base_url}/weather"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "imperial"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "temp": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"].get("speed", 0),
                "wind_direction": data["wind"].get("deg", 0),
                "precipitation": data.get("rain", {}).get("1h", 0) or 
                               data.get("snow", {}).get("1h", 0),
                "conditions": data["weather"][0]["main"].lower(),
                "description": data["weather"][0]["description"],
                "visibility": data.get("visibility", 10000) / 1000,
                "pressure": data["main"]["pressure"],
                "location": f"({lat}, {lon})"
            }
        except Exception as e:
            print(f"Error fetching weather: {e}")
            return self._get_mock_weather()
    
    def get_weather_for_game_date(
        self,
        city: str,
        state: Optional[str] = None,
        country: str = "US",
        game_date: Optional[datetime] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None
    ) -> Optional[Dict]:
        """
        Get weather forecast for a specific game date and location
        
        Args:
            city: City name
            state: State/Province
            country: Country code
            game_date: Date/time of the game
            lat: Latitude (optional, more accurate)
            lon: Longitude (optional, more accurate)
        
        Returns:
            Dictionary with weather data for the game date
        """
        from datetime import datetime, timedelta
        
        # If no game date provided, get current weather
        if not game_date:
            if lat and lon:
                return self.get_weather_for_coordinates(lat, lon)
            else:
                return self.get_weather_for_location(city, state, country)
        
        # Calculate days until game
        now = datetime.now()
        days_until_game = (game_date.date() - now.date()).days
        
        # If game is today or in the past, get current weather
        if days_until_game <= 0:
            if lat and lon:
                return self.get_weather_for_coordinates(lat, lon)
            else:
                return self.get_weather_for_location(city, state, country)
        
        # If game is more than 5 days away, use current weather (forecast limited)
        if days_until_game > 5:
            if lat and lon:
                return self.get_weather_for_coordinates(lat, lon)
            else:
                return self.get_weather_for_location(city, state, country)
        
        # Get forecast for the game date
        forecast = self.get_forecast(city, state, country, days=days_until_game + 1)
        
        if forecast and forecast.get("forecasts"):
            # Find the forecast closest to game time
            game_timestamp = game_date.timestamp()
            closest_forecast = None
            min_diff = float('inf')
            
            for fc in forecast["forecasts"]:
                diff = abs(fc["datetime"] - game_timestamp)
                if diff < min_diff:
                    min_diff = diff
                    closest_forecast = fc
            
            if closest_forecast:
                # Convert forecast to weather format
                return {
                    "temp": closest_forecast["temp"],
                    "feels_like": closest_forecast["temp"],  # Approximate
                    "humidity": 65,  # Default, forecast doesn't always include
                    "wind_speed": closest_forecast["wind_speed"],
                    "wind_direction": 0,  # Forecast doesn't always include
                    "precipitation": closest_forecast["precipitation"],
                    "conditions": closest_forecast["conditions"],
                    "description": closest_forecast["conditions"],
                    "visibility": 10,  # Default
                    "pressure": 1013,  # Default
                    "is_forecast": True,
                    "forecast_date": game_date.isoformat()
                }
        
        # Fallback to current weather
        location_str = f"{city}, {state}" if state else city
        if lat and lon:
            weather = self.get_weather_for_coordinates(lat, lon)
        else:
            weather = self.get_weather_for_location(city, state, country)
        
        # Ensure location is set
        if weather and "location" not in weather:
            weather["location"] = location_str
        
        return weather
    
    def get_forecast(
        self,
        city: str,
        state: Optional[str] = None,
        country: str = "US",
        days: int = 1
    ) -> Optional[Dict]:
        """
        Get weather forecast for upcoming days
        
        Args:
            city: City name
            state: State/Province
            country: Country code
            days: Number of days to forecast
        
        Returns:
            Dictionary with forecast data
        """
        if not self.api_key:
            return self._get_mock_forecast()
        
        try:
            location = f"{city},{state},{country}" if state else f"{city},{country}"
            url = f"{self.base_url}/forecast"
            params = {
                "q": location,
                "appid": self.api_key,
                "units": "imperial",
                "cnt": days * 8  # 8 forecasts per day (3-hour intervals)
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Process forecast data
            forecasts = []
            for item in data.get("list", [])[:days * 8]:
                forecasts.append({
                    "datetime": item["dt"],
                    "temp": item["main"]["temp"],
                    "wind_speed": item["wind"].get("speed", 0),
                    "precipitation": item.get("rain", {}).get("3h", 0) or 
                                   item.get("snow", {}).get("3h", 0),
                    "conditions": item["weather"][0]["main"].lower()
                })
            
            return {
                "location": data["city"]["name"],
                "forecasts": forecasts
            }
        except Exception as e:
            print(f"Error fetching forecast: {e}")
            return self._get_mock_forecast()
    
    def _get_mock_weather(self, location: str = "Game Location") -> Dict:
        """Return mock weather data for development"""
        return {
            "temp": 72,
            "feels_like": 70,
            "humidity": 65,
            "wind_speed": 8,
            "wind_direction": 180,
            "precipitation": 0,
            "conditions": "clear",
            "description": "clear sky",
            "visibility": 10,
            "pressure": 1013,
            "location": location
        }
    
    def _get_mock_forecast(self) -> Dict:
        """Return mock forecast data for development"""
        return {
            "location": "Mock City",
            "forecasts": [
                {
                    "datetime": 1234567890,
                    "temp": 72,
                    "wind_speed": 8,
                    "precipitation": 0,
                    "conditions": "clear"
                }
            ]
        }
    
    def analyze_weather_impact(
        self,
        weather: Dict,
        sport_type: str = "football"
    ) -> Dict:
        """
        Analyze how weather impacts the game
        
        Args:
            weather: Weather data dictionary
            sport_type: Type of sport (football, baseball, etc.)
        
        Returns:
            Dictionary with impact analysis
        """
        impact = {
            "overall_impact": "neutral",
            "factors": [],
            "severity": "low"
        }
        
        # Wind impact
        wind_speed = weather.get("wind_speed", 0)
        if wind_speed > 25:
            impact["factors"].append("Very high wind - major impact on passing")
            impact["severity"] = "high"
            impact["overall_impact"] = "negative_passing"
        elif wind_speed > 15:
            impact["factors"].append("High wind - moderate impact on passing")
            impact["severity"] = "moderate"
        
        # Precipitation impact
        precipitation = weather.get("precipitation", 0)
        if precipitation > 0.5:
            impact["factors"].append("Heavy precipitation - favors ground game")
            impact["severity"] = "high"
            if impact["overall_impact"] == "neutral":
                impact["overall_impact"] = "negative_passing"
        elif precipitation > 0:
            impact["factors"].append("Light precipitation - slight impact")
            impact["severity"] = "moderate"
        
        # Temperature impact
        temp = weather.get("temp", 70)
        if temp < 32:
            impact["factors"].append("Freezing temperatures - ball handling issues")
            impact["severity"] = "moderate"
        elif temp > 90:
            impact["factors"].append("Extreme heat - player fatigue factor")
            impact["severity"] = "moderate"
        
        return impact

