"""
API routes for game data
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.data.sports_data import SportsDataCollector

router = APIRouter()
data_collector = SportsDataCollector()


@router.get("/")
async def get_upcoming_games(
    sport: str = "nfl",
    days_ahead: int = 7
) -> List[dict]:
    """
    Get upcoming games
    
    Args:
        sport: Sport type (nfl, nba, mlb, etc.)
        days_ahead: Number of days to look ahead
    
    Returns:
        List of upcoming games
    """
    try:
        games = data_collector.get_upcoming_games(sport, days_ahead)
        return games
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{game_id}")
async def get_game_details(game_id: str) -> dict:
    """
    Get detailed information about a specific game
    
    Args:
        game_id: Unique game identifier
    
    Returns:
        Game details
    """
    game = data_collector.get_game_details(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


@router.get("/{game_id}/teams")
async def get_team_stats_for_game(game_id: str) -> dict:
    """
    Get statistics for both teams in a game
    
    Args:
        game_id: Unique game identifier
    
    Returns:
        Dictionary with home and away team statistics
    """
    game = data_collector.get_game_details(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    home_stats = data_collector.get_team_stats(game["home_team"], game.get("sport", "nfl"))
    away_stats = data_collector.get_team_stats(game["away_team"], game.get("sport", "nfl"))
    
    return {
        "game_id": game_id,
        "home_team_stats": home_stats,
        "away_team_stats": away_stats
    }

