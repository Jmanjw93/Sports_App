"""
API routes for betting odds
"""
from fastapi import APIRouter, HTTPException
from app.data.odds_collector import OddsCollector
from app.data.sports_data import SportsDataCollector

router = APIRouter()
odds_collector = OddsCollector()
data_collector = SportsDataCollector()


@router.get("/game/{game_id}")
async def get_game_odds(game_id: str) -> dict:
    """
    Get betting odds for a game from all platforms
    
    Args:
        game_id: Unique game identifier
    
    Returns:
        Dictionary with odds from bet365, DraftKings, and TheScore Bet
    """
    try:
        game = data_collector.get_game_details(game_id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        
        odds = odds_collector.get_odds_for_game(
            game_id,
            game["home_team"],
            game["away_team"],
            game.get("sport", "nfl")
        )
        
        # Find best odds
        best_odds = odds_collector.find_best_odds(odds, "team_win")
        
        return {
            "game_id": game_id,
            "home_team": game["home_team"],
            "away_team": game["away_team"],
            "odds_by_platform": odds,
            "best_odds": best_odds
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/player/{player_name}")
async def get_player_prop_odds(
    player_name: str,
    prop_type: str = "points",
    game_id: str = None
) -> dict:
    """
    Get player prop odds from all platforms
    
    Args:
        player_name: Player name
        prop_type: Type of prop (points, yards, etc.)
        game_id: Optional game identifier
    
    Returns:
        Dictionary with odds from all platforms
    """
    try:
        if not game_id:
            raise HTTPException(
                status_code=400, 
                detail="game_id is required for player props"
            )
        
        odds = odds_collector.get_player_prop_odds(
            player_name,
            prop_type,
            game_id,
            "nfl"  # Default, could be determined from game
        )
        
        return {
            "player_name": player_name,
            "prop_type": prop_type,
            "game_id": game_id,
            "odds_by_platform": odds
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

