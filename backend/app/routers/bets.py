"""
API routes for best betting opportunities
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.models.betting_models import BettingAnalyzer
from app.models.prediction_models import GamePredictor, PlayerPropPredictor
from app.models.weather_analyzer import WeatherAnalyzer
from app.data.sports_data import SportsDataCollector
from app.data.odds_collector import OddsCollector
from app.data.injury_data import InjuryDataCollector

router = APIRouter()
betting_analyzer = BettingAnalyzer()
game_predictor = GamePredictor()
player_predictor = PlayerPropPredictor()
weather_analyzer = WeatherAnalyzer()
data_collector = SportsDataCollector()
odds_collector = OddsCollector()
injury_collector = InjuryDataCollector()


@router.get("/best-bets")
async def get_best_bets(
    sport: str = "nfl",
    limit: int = 10
) -> dict:
    """
    Get the best betting opportunities across all games
    
    Args:
        sport: Sport type
        limit: Maximum number of bets to return
    
    Returns:
        Dictionary with best betting opportunities
    """
    try:
        # Get upcoming games
        games = data_collector.get_upcoming_games(sport, days_ahead=7)
        
        best_bets = []
        
        for game in games[:limit * 2]:  # Check more games than needed
            game_id = game["game_id"]
            
            # Get prediction
            try:
                # Get team stats
                home_stats = data_collector.get_team_stats(
                    game["home_team"], sport
                )
                away_stats = data_collector.get_team_stats(
                    game["away_team"], sport
                )
                
                # Get weather
                weather_data = None
                if "location" in game:
                    location = game["location"]
                    if "city" in location:
                        weather_data = weather_analyzer.get_weather_for_location(
                            location["city"],
                            location.get("state"),
                            location.get("country", "US")
                        )
                
                # Get injury data
                home_injuries = injury_collector.get_team_injuries(
                    game["home_team"], sport
                )
                away_injuries = injury_collector.get_team_injuries(
                    game["away_team"], sport
                )
                
                # Make prediction
                prediction = game_predictor.predict_game(
                    game["home_team"],
                    game["away_team"],
                    home_stats,
                    away_stats,
                    weather_data,
                    game_id,
                    home_injuries,
                    away_injuries
                )
                
                # Get odds
                odds_data = odds_collector.get_odds_for_game(
                    game_id,
                    game["home_team"],
                    game["away_team"],
                    sport
                )
                
                # Analyze bets for each platform
                for platform, odds in odds_data.items():
                    if not odds.get("available", False):
                        continue
                    
                    # Analyze home team bet
                    if odds.get("home_team_odds"):
                        home_opportunity = betting_analyzer.analyze_bet(
                            prediction.home_win_probability,
                            odds["home_team_odds"],
                            "team_win",
                            game["home_team"],
                            platform
                        )
                        
                        if home_opportunity.expected_value > 0:
                            best_bets.append({
                                "game_id": game_id,
                                "bet_type": "team_win",
                                "selection": game["home_team"],
                                "platform": platform,
                                "odds": home_opportunity.odds,
                                "expected_value": round(home_opportunity.expected_value, 3),
                                "kelly_percentage": round(home_opportunity.kelly_percentage, 3),
                                "recommendation": home_opportunity.recommendation,
                                "true_probability": round(home_opportunity.true_probability, 3),
                                "implied_probability": round(home_opportunity.implied_probability, 3)
                            })
                    
                    # Analyze away team bet
                    if odds.get("away_team_odds"):
                        away_opportunity = betting_analyzer.analyze_bet(
                            prediction.away_win_probability,
                            odds["away_team_odds"],
                            "team_win",
                            game["away_team"],
                            platform
                        )
                        
                        if away_opportunity.expected_value > 0:
                            best_bets.append({
                                "game_id": game_id,
                                "bet_type": "team_win",
                                "selection": game["away_team"],
                                "platform": platform,
                                "odds": away_opportunity.odds,
                                "expected_value": round(away_opportunity.expected_value, 3),
                                "kelly_percentage": round(away_opportunity.kelly_percentage, 3),
                                "recommendation": away_opportunity.recommendation,
                                "true_probability": round(away_opportunity.true_probability, 3),
                                "implied_probability": round(away_opportunity.implied_probability, 3)
                            })
            except Exception as e:
                # Skip games with errors
                continue
        
        # Sort by expected value and return top bets
        best_bets.sort(key=lambda x: x["expected_value"], reverse=True)
        
        return {
            "sport": sport,
            "total_opportunities": len(best_bets),
            "best_bets": best_bets[:limit]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/player-bets/{game_id}")
async def get_best_player_bets(
    game_id: str,
    limit: int = 5
) -> dict:
    """
    Get best player prop bets for a game
    
    Args:
        game_id: Game identifier
        limit: Maximum number of bets to return
    
    Returns:
        Dictionary with best player prop bets
    """
    try:
        game = data_collector.get_game_details(game_id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        
        # Mock player list - in production, get from game data
        players = [
            {"name": "Patrick Mahomes", "props": ["points", "yards", "touchdowns"]},
            {"name": "Josh Allen", "props": ["points", "yards", "touchdowns"]},
        ]
        
        best_bets = []
        
        for player_info in players:
            player_name = player_info["name"]
            
            for prop_type in player_info["props"]:
                try:
                    # Get player prediction
                    player_stats = data_collector.get_player_stats(
                        player_name, game.get("sport", "nfl")
                    )
                    opponent_stats = data_collector.get_team_stats(
                        game["away_team"], game.get("sport", "nfl")
                    )
                    
                    historical_avg = player_stats.get(f"{prop_type}_avg", 0)
                    
                    # Get odds first to get the line
                    odds_data = odds_collector.get_player_prop_odds(
                        player_name, prop_type, game_id, game.get("sport", "nfl")
                    )
                    
                    # Use line from first available platform
                    line = None
                    for platform_odds in odds_data.values():
                        if platform_odds.get("available") and platform_odds.get("line"):
                            line = platform_odds["line"]
                            break
                    
                    if not line:
                        continue
                    
                    # Make prediction
                    prediction = player_predictor.predict_player_prop(
                        player_name,
                        prop_type,
                        player_stats,
                        opponent_stats,
                        historical_avg,
                        line
                    )
                    
                    # Analyze bets for each platform
                    for platform, platform_odds in odds_data.items():
                        if not platform_odds.get("available", False):
                            continue
                        
                        # Analyze over bet
                        if platform_odds.get("over_odds"):
                            over_opportunity = betting_analyzer.analyze_bet(
                                prediction.over_probability,
                                platform_odds["over_odds"],
                                f"player_{prop_type}_over",
                                f"{player_name} {prop_type} Over {line}",
                                platform
                            )
                            
                            if over_opportunity.expected_value > 0:
                                best_bets.append({
                                    "game_id": game_id,
                                    "player_name": player_name,
                                    "bet_type": f"{prop_type}_over",
                                    "line": line,
                                    "platform": platform,
                                    "odds": over_opportunity.odds,
                                    "expected_value": round(over_opportunity.expected_value, 3),
                                    "kelly_percentage": round(over_opportunity.kelly_percentage, 3),
                                    "recommendation": over_opportunity.recommendation,
                                    "true_probability": round(over_opportunity.true_probability, 3)
                                })
                        
                        # Analyze under bet
                        if platform_odds.get("under_odds"):
                            under_opportunity = betting_analyzer.analyze_bet(
                                prediction.under_probability,
                                platform_odds["under_odds"],
                                f"player_{prop_type}_under",
                                f"{player_name} {prop_type} Under {line}",
                                platform
                            )
                            
                            if under_opportunity.expected_value > 0:
                                best_bets.append({
                                    "game_id": game_id,
                                    "player_name": player_name,
                                    "bet_type": f"{prop_type}_under",
                                    "line": line,
                                    "platform": platform,
                                    "odds": under_opportunity.odds,
                                    "expected_value": round(under_opportunity.expected_value, 3),
                                    "kelly_percentage": round(under_opportunity.kelly_percentage, 3),
                                    "recommendation": under_opportunity.recommendation,
                                    "true_probability": round(under_opportunity.true_probability, 3)
                                })
                except Exception:
                    continue
        
        # Sort by expected value
        best_bets.sort(key=lambda x: x["expected_value"], reverse=True)
        
        return {
            "game_id": game_id,
            "total_opportunities": len(best_bets),
            "best_player_bets": best_bets[:limit]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

