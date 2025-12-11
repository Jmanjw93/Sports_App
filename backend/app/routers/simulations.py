"""
Monte Carlo simulation engine for game outcomes
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Optional
import random
import numpy as np

router = APIRouter()


@router.get("/simulate-game/{game_id}")
async def simulate_game(
    game_id: str,
    num_simulations: int = 10000
) -> dict:
    """
    Run Monte Carlo simulation for a game outcome
    
    Args:
        game_id: Game identifier
        num_simulations: Number of simulations to run (default 10,000)
    
    Returns:
        Simulation results with win probabilities and distribution
    """
    try:
        from app.data.sports_data import SportsDataCollector
        from app.routers.predictions import get_game_prediction
        
        # Get game prediction
        prediction_response = await get_game_prediction(game_id)
        
        home_win_prob = prediction_response.get("home_win_probability", 0.5)
        away_win_prob = prediction_response.get("away_win_probability", 0.5)
        
        # Run simulations
        home_wins = 0
        away_wins = 0
        score_differences = []
        
        for _ in range(num_simulations):
            # Simulate game outcome
            rand = random.random()
            if rand < home_win_prob:
                home_wins += 1
                # Simulate score difference (home win)
                score_diff = np.random.normal(7, 10)  # Mean 7, std 10
                score_differences.append(score_diff)
            else:
                away_wins += 1
                # Simulate score difference (away win)
                score_diff = np.random.normal(-7, 10)
                score_differences.append(score_diff)
        
        # Calculate statistics
        home_win_rate = home_wins / num_simulations
        away_win_rate = away_wins / num_simulations
        
        # Score distribution
        score_diffs_array = np.array(score_differences)
        mean_score_diff = np.mean(score_diffs_array)
        std_score_diff = np.std(score_diffs_array)
        
        # Calculate percentiles
        percentiles = {
            "p5": float(np.percentile(score_diffs_array, 5)),
            "p25": float(np.percentile(score_diffs_array, 25)),
            "p50": float(np.percentile(score_diffs_array, 50)),
            "p75": float(np.percentile(score_diffs_array, 75)),
            "p95": float(np.percentile(score_diffs_array, 95))
        }
        
        # Confidence intervals
        confidence_95_lower = mean_score_diff - 1.96 * std_score_diff
        confidence_95_upper = mean_score_diff + 1.96 * std_score_diff
        
        return {
            "game_id": game_id,
            "num_simulations": num_simulations,
            "home_team": prediction_response.get("home_team"),
            "away_team": prediction_response.get("away_team"),
            "simulated_win_probabilities": {
                "home": round(home_win_rate, 4),
                "away": round(away_win_rate, 4)
            },
            "predicted_win_probabilities": {
                "home": home_win_prob,
                "away": away_win_prob
            },
            "score_difference_stats": {
                "mean": round(mean_score_diff, 2),
                "std": round(std_score_diff, 2),
                "percentiles": percentiles,
                "confidence_95": {
                    "lower": round(confidence_95_lower, 2),
                    "upper": round(confidence_95_upper, 2)
                }
            },
            "simulation_results": {
                "home_wins": home_wins,
                "away_wins": away_wins
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/simulate-season")
async def simulate_season(
    team: str,
    sport: str = "nfl",
    num_simulations: int = 1000
) -> dict:
    """
    Simulate a team's season outcomes
    
    Args:
        team: Team name
        sport: Sport type
        num_simulations: Number of season simulations
    
    Returns:
        Season simulation results
    """
    try:
        # Mock season simulation
        wins_distribution = []
        playoff_appearances = 0
        championship_wins = 0
        
        for _ in range(num_simulations):
            # Simulate season wins (assuming 17 games for NFL, 82 for NBA, etc.)
            games = 17 if sport == "nfl" else 82 if sport == "nba" else 162 if sport == "mlb" else 82
            wins = np.random.binomial(games, 0.55)  # 55% win probability as base
            wins_distribution.append(wins)
            
            # Playoff appearance (top 50% of teams)
            if wins >= games * 0.5:
                playoff_appearances += 1
            
            # Championship (top 10% of playoff teams)
            if wins >= games * 0.6 and random.random() < 0.1:
                championship_wins += 1
        
        wins_array = np.array(wins_distribution)
        
        return {
            "team": team,
            "sport": sport,
            "num_simulations": num_simulations,
            "expected_wins": round(float(np.mean(wins_array)), 2),
            "wins_distribution": {
                "min": int(np.min(wins_array)),
                "max": int(np.max(wins_array)),
                "mean": round(float(np.mean(wins_array)), 2),
                "std": round(float(np.std(wins_array)), 2),
                "percentiles": {
                    "p10": int(np.percentile(wins_array, 10)),
                    "p25": int(np.percentile(wins_array, 25)),
                    "p50": int(np.percentile(wins_array, 50)),
                    "p75": int(np.percentile(wins_array, 75)),
                    "p90": int(np.percentile(wins_array, 90))
                }
            },
            "playoff_probability": round(playoff_appearances / num_simulations, 4),
            "championship_probability": round(championship_wins / num_simulations, 4)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




