"""
API routes for game and player predictions
"""
from fastapi import APIRouter, HTTPException
from typing import Optional
from app.models.prediction_models import GamePredictor, PlayerPropPredictor
from app.models.weather_analyzer import WeatherAnalyzer
from app.data.sports_data import SportsDataCollector
from app.data.injury_data import InjuryDataCollector

router = APIRouter()
game_predictor = GamePredictor()
player_predictor = PlayerPropPredictor()
weather_analyzer = WeatherAnalyzer()
data_collector = SportsDataCollector()
injury_collector = InjuryDataCollector()


@router.get("/game/{game_id}")
async def get_game_prediction(game_id: str) -> dict:
    """
    Get prediction for a game outcome
    
    Args:
        game_id: Unique game identifier
    
    Returns:
        Game prediction with probabilities
    """
    try:
        # Get game details
        game = data_collector.get_game_details(game_id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        
        # Get team statistics
        home_stats = data_collector.get_team_stats(
            game["home_team"], 
            game.get("sport", "nfl")
        )
        away_stats = data_collector.get_team_stats(
            game["away_team"],
            game.get("sport", "nfl")
        )
        
        # Get weather data for the game location and date
        weather_data = None
        if "location" in game:
            location = game["location"]
            
            # Parse game date for forecast
            game_date = None
            if "date" in game:
                try:
                    from datetime import datetime
                    game_date = datetime.fromisoformat(game["date"].replace("Z", "+00:00"))
                except:
                    try:
                        from datetime import datetime
                        game_date = datetime.fromisoformat(game["date"])
                    except:
                        pass
            
            # Log which location is being used for weather
            location_str = f"{location.get('city', 'Unknown')}, {location.get('state', '')}"
            if "lat" in location and "lon" in location:
                print(f"Fetching weather for game at {location_str} (coordinates: {location['lat']}, {location['lon']})")
                weather_data = weather_analyzer.get_weather_for_game_date(
                    location.get("city", ""),
                    location.get("state"),
                    location.get("country", "US"),
                    game_date,
                    location["lat"],
                    location["lon"]
                )
            elif "city" in location:
                print(f"Fetching weather for game at {location_str}")
                weather_data = weather_analyzer.get_weather_for_game_date(
                    location["city"],
                    location.get("state"),
                    location.get("country", "US"),
                    game_date
                )
            
            # Add location info to weather data if not present
            if weather_data and "location" not in weather_data:
                weather_data["location"] = location_str
        
        # Get injury data for both teams
        home_injuries = injury_collector.get_team_injuries(
            game["home_team"], game.get("sport", "nfl")
        )
        away_injuries = injury_collector.get_team_injuries(
            game["away_team"], game.get("sport", "nfl")
        )
        
        # Get player props to enhance prediction (optional but recommended)
        player_prop_data = None
        try:
            # Import the internal player props function
            from app.routers.player_props import _get_game_player_props_internal
            player_prop_data = await _get_game_player_props_internal(game_id)
        except Exception as e:
            # If player props fail, continue without them
            print(f"Could not fetch player props: {e}")
        
        # Make prediction
        sport = game.get("sport", "nfl")
        prediction = game_predictor.predict_game(
            game["home_team"],
            game["away_team"],
            home_stats,
            away_stats,
            weather_data,
            game_id,
            home_injuries,
            away_injuries,
            sport
        )
        
        # Apply player prop adjustments if available
        player_prop_adjustment = None
        if player_prop_data:
            player_prop_adjustment = game_predictor.analyze_player_props_for_game(
                game["home_team"],
                game["away_team"],
                player_prop_data.get("home_team_props", []),
                player_prop_data.get("away_team_props", [])
            )
            
            # Adjust probabilities based on player prop insights
            net_adjustment = player_prop_adjustment.get("net_adjustment", 0.0)
            prediction.home_win_probability += net_adjustment
            prediction.away_win_probability = 1.0 - prediction.home_win_probability
            
            # Ensure probabilities stay in valid range
            prediction.home_win_probability = max(0.1, min(0.9, prediction.home_win_probability))
            prediction.away_win_probability = 1.0 - prediction.home_win_probability
            
            # Recalculate confidence
            prediction.confidence = abs(prediction.home_win_probability - prediction.away_win_probability)
            
            # Update key factors
            if net_adjustment > 0.02:
                prediction.key_factors.append(
                    f"Home team key players have favorable historical matchups (+{net_adjustment*100:.1f}% advantage)"
                )
            elif net_adjustment < -0.02:
                prediction.key_factors.append(
                    f"Away team key players have favorable historical matchups ({abs(net_adjustment)*100:.1f}% advantage)"
                )
        
        # Convert to dict for JSON response
        response = {
            "game_id": prediction.game_id,
            "home_team": prediction.home_team,
            "away_team": prediction.away_team,
            "predicted_winner": prediction.predicted_winner,
            "home_win_probability": round(prediction.home_win_probability, 3),
            "away_win_probability": round(prediction.away_win_probability, 3),
            "confidence": round(prediction.confidence, 3),
            "weather_impact": prediction.weather_impact,
            "injury_impact": prediction.injury_impact,
            "coaching_impact": prediction.coaching_impact,
            "key_factors": prediction.key_factors
        }
        
        # Add player prop adjustment if available
        if player_prop_adjustment:
            response["player_prop_adjustment"] = player_prop_adjustment
        
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/coaching-matchup")
async def get_coaching_matchup(
    home_team: str,
    away_team: str,
    sport: str = "nfl"
) -> dict:
    """
    Get detailed coaching matchup information including win/loss records
    
    Args:
        home_team: Home team name
        away_team: Away team name
        sport: Sport type (nfl, nba, mlb, nhl)
    
    Returns:
        Detailed coaching matchup with win/loss records
    """
    try:
        from app.data.historical_matchups import HistoricalMatchupAnalyzer
        matchup_analyzer = HistoricalMatchupAnalyzer()
        
        coaching_matchup = matchup_analyzer.analyze_coaching_matchup(
            home_team, away_team, sport
        )
        
        return {
            "home_team": home_team,
            "away_team": away_team,
            "sport": sport,
            "home_coach": coaching_matchup["home_coach"],
            "away_coach": coaching_matchup["away_coach"],
            "historical_record": coaching_matchup["historical_record"],
            "adjustment_factor": coaching_matchup["adjustment_factor"],
            "key_insight": coaching_matchup["key_insight"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/player/{player_name}")
async def get_player_prop_prediction(
    player_name: str,
    prop_type: str = "points",
    game_id: Optional[str] = None,
    line: Optional[float] = None
) -> dict:
    """
    Get prediction for a player prop bet
    
    Args:
        player_name: Player name
        prop_type: Type of prop (points, assists, yards, etc.)
        game_id: Optional game identifier
        line: Optional betting line
    
    Returns:
        Player prop prediction
    """
    try:
        # Get player statistics
        sport = "nfl"  # Default, could be determined from game_id
        if game_id:
            game = data_collector.get_game_details(game_id)
            if game:
                sport = game.get("sport", "nfl")
        
        player_stats = data_collector.get_player_stats(player_name, sport)
        
        # Get opponent stats if game_id provided
        opponent_stats = {}
        if game_id:
            game = data_collector.get_game_details(game_id)
            if game:
                # Determine opponent
                # This is simplified - in production, determine based on player's team
                opponent_stats = data_collector.get_team_stats(
                    game["away_team"], sport
                )
        
        # Historical average
        historical_avg = player_stats.get(f"{prop_type}_avg", 0)
        
        # Make prediction
        prediction = player_predictor.predict_player_prop(
            player_name,
            prop_type,
            player_stats,
            opponent_stats,
            historical_avg,
            line
        )
        
        return {
            "player_name": prediction.player_name,
            "prop_type": prediction.prop_type,
            "predicted_value": round(prediction.predicted_value, 2),
            "over_probability": round(prediction.over_probability, 3),
            "under_probability": round(prediction.under_probability, 3),
            "confidence": round(prediction.confidence, 3),
            "historical_avg": round(prediction.historical_avg, 2),
            "matchup_factor": round(prediction.matchup_factor, 3)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

