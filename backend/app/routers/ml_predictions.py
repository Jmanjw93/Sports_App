"""
API routes for ML-based predictions
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.models.advanced_ml_models import AdvancedMLPredictor, PlayerPropMLPredictor
from app.models.weather_analyzer import WeatherAnalyzer
from app.data.sports_data import SportsDataCollector
from app.data.injury_data import InjuryDataCollector
from app.cache.redis_cache import get_cache, cached
from app.monitoring.prometheus_metrics import record_prediction
from app.utils.data_normalizer import DataNormalizer

router = APIRouter()
ml_predictor = AdvancedMLPredictor()
player_ml_predictor = PlayerPropMLPredictor()
weather_analyzer = WeatherAnalyzer()
data_collector = SportsDataCollector()
injury_collector = InjuryDataCollector()
cache = get_cache()


@router.get("/game/{game_id}")
@cached(ttl=300, key_prefix="ml_prediction")
async def get_ml_game_prediction(
    game_id: str,
    model_type: str = Query("ensemble", description="Model type: random_forest, gradient_boosting, xgboost, logistic, ensemble")
) -> dict:
    """
    Get ML-based prediction for a game outcome
    
    Args:
        game_id: Unique game identifier
        model_type: Type of ML model to use
    
    Returns:
        ML-based game prediction with probabilities
    """
    try:
        # Validate model type
        valid_models = ["random_forest", "gradient_boosting", "xgboost", "logistic", "ensemble"]
        if model_type not in valid_models:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid model_type. Must be one of: {', '.join(valid_models)}"
            )
        
        # Get game details
        game = data_collector.get_game_details(game_id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        
        # Normalize game data
        game = DataNormalizer.normalize_game_data(game)
        sport = game.get("sport", "nfl")
        
        # Get team statistics
        home_stats_raw = data_collector.get_team_stats(game["home_team"], sport)
        away_stats_raw = data_collector.get_team_stats(game["away_team"], sport)
        
        # Normalize stats
        home_stats = DataNormalizer.normalize_team_stats(home_stats_raw, sport)
        away_stats = DataNormalizer.normalize_team_stats(away_stats_raw, sport)
        
        # Get weather data
        weather_data = None
        if "location" in game:
            location = game["location"]
            game_date = None
            if "date" in game:
                try:
                    from datetime import datetime
                    game_date = datetime.fromisoformat(game["date"].replace("Z", "+00:00"))
                except:
                    pass
            
            if "lat" in location and "lon" in location:
                weather_data = weather_analyzer.get_weather_for_game_date(
                    location.get("city", ""),
                    location.get("state"),
                    location.get("country", "US"),
                    game_date,
                    location["lat"],
                    location["lon"]
                )
            elif "city" in location:
                weather_data = weather_analyzer.get_weather_for_game_date(
                    location["city"],
                    location.get("state"),
                    location.get("country", "US"),
                    game_date
                )
            
            if weather_data:
                weather_data = DataNormalizer.normalize_weather_data(weather_data)
        
        # Get injury data
        home_injuries = injury_collector.get_team_injuries(game["home_team"], sport)
        away_injuries = injury_collector.get_team_injuries(game["away_team"], sport)
        
        injury_data = {
            "home_injuries": home_injuries,
            "away_injuries": away_injuries
        }
        
        # Make ML prediction
        prediction = ml_predictor.predict_game_ml(
            game["home_team"],
            game["away_team"],
            home_stats,
            away_stats,
            sport=sport,
            weather_data=weather_data,
            injury_data=injury_data,
            model_type=model_type
        )
        
        # Record metrics
        record_prediction(sport, model_type, prediction["confidence"])
        
        # Build response
        response = {
            "game_id": game_id,
            "home_team": game["home_team"],
            "away_team": game["away_team"],
            "predicted_winner": prediction["predicted_winner"],
            "home_win_probability": round(prediction["home_win_probability"], 3),
            "away_win_probability": round(prediction["away_win_probability"], 3),
            "confidence": round(prediction["confidence"], 3),
            "model_type": prediction["model_type"],
            "features_used": prediction["features_used"],
            "weather_data": weather_data,
            "injury_data": injury_data
        }
        
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/player/{player_name}")
@cached(ttl=300, key_prefix="ml_player_prop")
async def get_ml_player_prop_prediction(
    player_name: str,
    prop_type: str = Query("points", description="Type of prop: points, yards, touchdowns, etc."),
    game_id: Optional[str] = None,
    line: Optional[float] = None
) -> dict:
    """
    Get ML-based prediction for a player prop bet
    
    Args:
        player_name: Player name
        prop_type: Type of prop (points, yards, touchdowns, etc.)
        game_id: Optional game identifier
        line: Optional betting line
    
    Returns:
        ML-based player prop prediction
    """
    try:
        # Determine sport
        sport = "nfl"
        if game_id:
            game = data_collector.get_game_details(game_id)
            if game:
                sport = game.get("sport", "nfl")
        
        # Get player statistics
        player_stats_raw = data_collector.get_player_stats(player_name, sport)
        player_stats = DataNormalizer.normalize_player_stats(player_stats_raw, sport)
        
        # Get opponent stats if game_id provided
        opponent_stats = {}
        if game_id:
            game = data_collector.get_game_details(game_id)
            if game:
                # Determine opponent (simplified)
                opponent_stats_raw = data_collector.get_team_stats(
                    game["away_team"], sport
                )
                opponent_stats = DataNormalizer.normalize_team_stats(opponent_stats_raw, sport)
        
        # Historical average
        historical_avg = player_stats.get(f"{prop_type}_avg", 0)
        
        # Make ML prediction
        prediction = player_ml_predictor.predict_player_prop_ml(
            player_name,
            prop_type,
            player_stats,
            opponent_stats,
            historical_avg,
            line
        )
        
        # Record metrics
        record_prediction(sport, "player_prop_ml", prediction["confidence"])
        
        return {
            "player_name": prediction["player_name"],
            "prop_type": prediction["prop_type"],
            "predicted_value": round(prediction["predicted_value"], 2),
            "over_probability": round(prediction["over_probability"], 3),
            "under_probability": round(prediction["under_probability"], 3),
            "confidence": round(prediction["confidence"], 3),
            "historical_avg": round(prediction["historical_avg"], 2),
            "matchup_factor": round(prediction["matchup_factor"], 3),
            "model_type": "ml"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

