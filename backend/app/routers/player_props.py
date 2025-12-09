"""
API routes for player props
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.models.prediction_models import PlayerPropPredictor
from app.data.sports_data import SportsDataCollector
from app.data.odds_collector import OddsCollector
from app.data.injury_data import InjuryDataCollector
from app.data.historical_matchups import HistoricalMatchupAnalyzer
from typing import Optional as Opt

router = APIRouter()
player_predictor = PlayerPropPredictor()
data_collector = SportsDataCollector()
odds_collector = OddsCollector()
injury_collector = InjuryDataCollector()
matchup_analyzer = HistoricalMatchupAnalyzer()


async def _get_game_player_props_internal(game_id: str) -> dict:
    """
    Internal function to get player props (can be called from other modules)
    """
    # Get game details
    game = data_collector.get_game_details(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    home_team = game["home_team"]
    away_team = game["away_team"]
    sport = game.get("sport", "nfl")
    
    # Get team stats
    home_stats = data_collector.get_team_stats(home_team, sport)
    away_stats = data_collector.get_team_stats(away_team, sport)
    
    # Get coaches for historical matchup analysis
    if sport == "nfl":
        home_coach = matchup_analyzer.get_team_coach(home_team, sport)
        away_coach = matchup_analyzer.get_team_coach(away_team, sport)
    else:
        home_coach = matchup_analyzer.get_team_coach_for_sport(home_team, sport)
        away_coach = matchup_analyzer.get_team_coach_for_sport(away_team, sport)
    
    # Get injuries for both teams
    home_injuries = injury_collector.get_team_injuries(home_team, sport)
    away_injuries = injury_collector.get_team_injuries(away_team, sport)
    
    # Get player stats for each team
    home_players = data_collector.get_team_players(home_team, sport)
    away_players = data_collector.get_team_players(away_team, sport)
    
    # Generate props for home team
    home_props = []
    for player in home_players[:5]:  # Top 5 players
        player_stats = data_collector.get_player_stats(player["name"], sport)
        
        # Check if player is injured
        player_injury = None
        for injury in home_injuries:
            if injury.player_name == player["name"]:
                player_injury = injury
                break
        
        # Get props for this player
        props = _generate_player_props(
            player["name"],
            player["position"],
            player_stats,
            away_stats,
            player_injury,
            sport,
            opponent_team=away_team,
            opponent_coach=away_coach
        )
        
        # Get odds for these props
        for prop in props:
            odds = odds_collector.get_player_prop_odds(
                player["name"], prop["prop_type"], game_id, sport
            )
            prop["odds"] = odds
        
        home_props.extend(props)
    
    # Generate props for away team
    away_props = []
    for player in away_players[:5]:  # Top 5 players
        player_stats = data_collector.get_player_stats(player["name"], sport)
        
        # Check if player is injured
        player_injury = None
        for away_injury in away_injuries:
            if away_injury.player_name == player["name"]:
                player_injury = away_injury
                break
        
        # Get props for this player
        props = _generate_player_props(
            player["name"],
            player["position"],
            player_stats,
            home_stats,
            player_injury,
            sport,
            opponent_team=home_team,
            opponent_coach=home_coach
        )
        
        # Get odds for these props
        for prop in props:
            odds = odds_collector.get_player_prop_odds(
                player["name"], prop["prop_type"], game_id, sport
            )
            prop["odds"] = odds
        
        away_props.extend(props)
    
    return {
        "game_id": game_id,
        "home_team": home_team,
        "away_team": away_team,
        "home_team_props": home_props,
        "away_team_props": away_props
    }


@router.get("/game/{game_id}")
async def get_game_player_props(game_id: str) -> dict:
    """
    Get player props for a game, separated by team
    
    Args:
        game_id: Unique game identifier
    
    Returns:
        Dictionary with home_team_props and away_team_props
    """
    try:
        return await _get_game_player_props_internal(game_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _generate_player_props(
    player_name: str,
    position: str,
    player_stats: dict,
    opponent_stats: dict,
    injury: Opt,
    sport: str,
    opponent_team: Optional[str] = None,
    opponent_coach: Optional[str] = None
) -> List[dict]:
    """Generate player props based on position and stats"""
    props = []
    
    if sport == "nfl":
        if position == "QB":
            # Passing yards (season average per game)
            season_avg_yards = player_stats.get("yards_avg", 250)
            props.append({
                "player_name": player_name,
                "position": position,
                "prop_type": "passing_yards",
                "prop_name": "Passing Yards",
                "line": season_avg_yards,  # Line is typically set near season average
                "predicted_value": season_avg_yards,  # Will be adjusted in prediction
                "unit": "yards"
            })
            # Passing touchdowns
            season_avg_tds = player_stats.get("touchdowns_avg", 2)
            props.append({
                "player_name": player_name,
                "position": position,
                "prop_type": "passing_touchdowns",
                "prop_name": "Passing TDs",
                "line": season_avg_tds,
                "predicted_value": season_avg_tds,
                "unit": "TDs"
            })
        elif position == "RB":
            # Rushing yards (season average per game)
            season_avg_rush_yards = player_stats.get("yards_avg", 80)
            props.append({
                "player_name": player_name,
                "position": position,
                "prop_type": "rushing_yards",
                "prop_name": "Rushing Yards",
                "line": season_avg_rush_yards,
                "predicted_value": season_avg_rush_yards,  # Will be adjusted in prediction
                "unit": "yards"
            })
            # Rushing touchdowns
            season_avg_rush_tds = player_stats.get("touchdowns_avg", 0.8)
            props.append({
                "player_name": player_name,
                "position": position,
                "prop_type": "rushing_touchdowns",
                "prop_name": "Rushing TDs",
                "line": season_avg_rush_tds,
                "predicted_value": season_avg_rush_tds,
                "unit": "TDs"
            })
        elif position == "WR" or position == "TE":
            # Receiving yards (season average per game)
            season_avg_rec_yards = player_stats.get("yards_avg", 60)
            props.append({
                "player_name": player_name,
                "position": position,
                "prop_type": "receiving_yards",
                "prop_name": "Receiving Yards",
                "line": season_avg_rec_yards,
                "predicted_value": season_avg_rec_yards,  # Will be adjusted in prediction
                "unit": "yards"
            })
            # Receptions
            season_avg_rec = player_stats.get("receptions_avg", 5)
            props.append({
                "player_name": player_name,
                "position": position,
                "prop_type": "receptions",
                "prop_name": "Receptions",
                "line": season_avg_rec,
                "predicted_value": season_avg_rec,
                "unit": "rec"
            })
    elif sport == "nba":
        # NBA player props
        if position in ["PG", "SG", "SF", "PF", "C"]:
            # Points
            season_avg_points = player_stats.get("points_avg", 20)
            props.append({
                "player_name": player_name,
                "position": position,
                "prop_type": "points",
                "prop_name": "Points",
                "line": season_avg_points,
                "predicted_value": season_avg_points,
                "unit": "pts"
            })
            # Assists (for guards/forwards)
            if position in ["PG", "SG", "SF"]:
                season_avg_assists = player_stats.get("assists_avg", 5)
                props.append({
                    "player_name": player_name,
                    "position": position,
                    "prop_type": "assists",
                    "prop_name": "Assists",
                    "line": season_avg_assists,
                    "predicted_value": season_avg_assists,
                    "unit": "ast"
                })
            # Rebounds (for forwards/centers)
            if position in ["PF", "C", "SF"]:
                season_avg_rebounds = player_stats.get("rebounds_avg", 7)
                props.append({
                    "player_name": player_name,
                    "position": position,
                    "prop_type": "rebounds",
                    "prop_name": "Rebounds",
                    "line": season_avg_rebounds,
                    "predicted_value": season_avg_rebounds,
                    "unit": "reb"
                })
    elif sport == "mlb":
        # MLB player props
        if position == "P":
            # Strikeouts for pitchers
            season_avg_so = player_stats.get("strikeouts_avg", 7)
            props.append({
                "player_name": player_name,
                "position": position,
                "prop_type": "strikeouts",
                "prop_name": "Strikeouts",
                "line": season_avg_so,
                "predicted_value": season_avg_so,
                "unit": "SO"
            })
        else:
            # Hits for batters
            season_avg_hits = player_stats.get("hits_avg", 1.2)
            props.append({
                "player_name": player_name,
                "position": position,
                "prop_type": "hits",
                "prop_name": "Hits",
                "line": season_avg_hits,
                "predicted_value": season_avg_hits,
                "unit": "H"
            })
            # Home runs
            season_avg_hr = player_stats.get("home_runs_avg", 0.3)
            props.append({
                "player_name": player_name,
                "position": position,
                "prop_type": "home_runs",
                "prop_name": "Home Runs",
                "line": season_avg_hr,
                "predicted_value": season_avg_hr,
                "unit": "HR"
            })
    elif sport == "nhl":
        # NHL player props
        if position == "G":
            # Saves for goalies
            season_avg_saves = player_stats.get("saves_avg", 28)
            props.append({
                "player_name": player_name,
                "position": position,
                "prop_type": "saves",
                "prop_name": "Saves",
                "line": season_avg_saves,
                "predicted_value": season_avg_saves,
                "unit": "saves"
            })
        else:
            # Points for skaters
            season_avg_points = player_stats.get("points_avg", 0.9)
            props.append({
                "player_name": player_name,
                "position": position,
                "prop_type": "points",
                "prop_name": "Points",
                "line": season_avg_points,
                "predicted_value": season_avg_points,
                "unit": "pts"
            })
            # Shots on goal
            season_avg_shots = player_stats.get("shots_avg", 3.5)
            props.append({
                "player_name": player_name,
                "position": position,
                "prop_type": "shots",
                "prop_name": "Shots on Goal",
                "line": season_avg_shots,
                "predicted_value": season_avg_shots,
                "unit": "SOG"
            })
    
    # Adjust for injuries
    if injury:
        injury_impact = 0.0
        if injury.status.code == "out":
            injury_impact = 1.0
        elif injury.status.code == "doubtful":
            injury_impact = 0.75
        elif injury.status.code == "questionable":
            injury_impact = 0.50
        elif injury.status.code == "probable":
            injury_impact = 0.25
        
        # Apply injury impact to predicted values
        for prop in props:
            prop["predicted_value"] = prop["predicted_value"] * (1 - injury_impact)
            prop["injury_status"] = injury.status.code
            prop["injury_type"] = injury.injury_type.code
    
    # Make predictions for each prop
    for prop in props:
        # Use historical average (season average per game) for prediction
        historical_avg = prop["line"]  # Line is typically set at season average
        
        prediction = player_predictor.predict_player_prop(
            player_name,
            prop["prop_type"],
            player_stats,
            opponent_stats,
            historical_avg,  # Pass season average
            prop["line"],  # Pass betting line
            position,  # Pass position for better predictions
            opponent_team,  # Pass opponent team for historical matchup
            opponent_coach  # Pass opponent coach for historical matchup
        )
        
        # Update with predicted value (adjusted for single game)
        prop["predicted_value"] = round(prediction.predicted_value, 1)
        prop["over_probability"] = round(prediction.over_probability, 3)
        prop["under_probability"] = round(prediction.under_probability, 3)
        prop["confidence"] = round(prediction.confidence, 3)
        prop["ev"] = prediction.expected_value if hasattr(prediction, 'expected_value') else 0.0
        
        # Add historical matchup data if available
        if prediction.historical_matchup_data:
            prop["historical_matchup"] = {
                "team_matchup_factor": prediction.historical_matchup_data.get("team_matchup_factor", 1.0),
                "coach_matchup_factor": prediction.historical_matchup_data.get("coach_matchup_factor", 1.0),
                "total_adjustment": prediction.historical_matchup_data.get("total_adjustment", 0.0),
                "historical_games": prediction.historical_matchup_data.get("historical_games", 0)
            }
    
    return props

