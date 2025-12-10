"""
API routes for player comparison with historical matchups
"""
from fastapi import APIRouter, HTTPException
from typing import Optional
from app.data.historical_matchups import HistoricalMatchupAnalyzer
from app.data.nfl_players import get_all_nfl_players, search_players, get_players_by_type

router = APIRouter()

# Initialize analyzer
matchup_analyzer = HistoricalMatchupAnalyzer()


@router.get("/compare")
async def compare_players(
    player1: str,
    player2: str,
    sport: str = "nfl",
    include_college: bool = True
) -> dict:
    """
    Compare two players with historical matchups and facts
    
    Args:
        player1: First player name
        player2: Second player name
        sport: Sport type (nfl, nba, mlb, nhl)
        include_college: Whether to include college matchups
    
    Returns:
        Comprehensive player comparison with historical data
    """
    try:
        # Get player vs player history
        matchup_history = matchup_analyzer.get_player_vs_player_history(
            player1, player2, sport, include_college
        )
        
        # Get player facts
        player1_facts = matchup_analyzer.get_player_facts(player1, sport)
        player2_facts = matchup_analyzer.get_player_facts(player2, sport)
        
        return {
            "player1": player1_facts,
            "player2": player2_facts,
            "head_to_head": matchup_history,
            "summary": {
                "total_matchups": matchup_history["total_games"],
                "player1_advantage": matchup_history["player1_win_rate"] > 0.5,
                "player2_advantage": matchup_history["player2_win_rate"] > 0.5,
                "even_matchup": abs(matchup_history["player1_win_rate"] - 0.5) < 0.1
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/player-facts/{player_name}")
async def get_player_facts(
    player_name: str,
    sport: str = "nfl"
) -> dict:
    """
    Get additional facts and information about a player
    
    Args:
        player_name: Player name
        sport: Sport type
    
    Returns:
        Player facts, achievements, and background
    """
    try:
        facts = matchup_analyzer.get_player_facts(player_name, sport)
        return facts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/matchup-history")
async def get_matchup_history(
    player1: str,
    player2: str,
    sport: str = "nfl",
    include_college: bool = True
) -> dict:
    """
    Get historical head-to-head matchups between two players
    
    Args:
        player1: First player name
        player2: Second player name
        sport: Sport type
        include_college: Whether to include college matchups
    
    Returns:
        Historical matchup data
    """
    try:
        history = matchup_analyzer.get_player_vs_player_history(
            player1, player2, sport, include_college
        )
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/players")
async def get_players(
    sport: str = "nfl",
    player_type: str = "all",
    search: Optional[str] = None
) -> dict:
    """
    Get all players for a sport, optionally filtered by type and search query
    
    Args:
        sport: Sport type (currently supports nfl)
        player_type: "offense", "defense", or "all"
        search: Optional search query to filter by name or team
    
    Returns:
        List of players matching criteria
    """
    try:
        if sport == "nfl":
            if search:
                players = search_players(search, player_type)
            else:
                players = get_players_by_type(player_type)
            
            return {
                "players": players,
                "total": len(players),
                "sport": sport,
                "player_type": player_type
            }
        else:
            # For other sports, return empty for now
            return {
                "players": [],
                "total": 0,
                "sport": sport,
                "player_type": player_type,
                "message": f"Player database for {sport} coming soon"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

