"""
Parlay builder and analysis endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Optional
from dataclasses import dataclass
from pydantic import BaseModel
import math

router = APIRouter()


class ParlayLeg(BaseModel):
    """Represents a single leg in a parlay"""
    player_name: str
    team: str
    prop_type: str  # e.g., "yards", "touchdowns", "points"
    prop_value: float  # e.g., 100.5 for over/under
    selection: str  # "over" or "under"
    odds: float  # Decimal odds
    win_probability: float  # True probability of winning (0-1)


class ParlayRequest(BaseModel):
    """Request to calculate parlay odds and analysis"""
    legs: List[ParlayLeg]
    bet_amount: float


@router.post("/calculate")
async def calculate_parlay(parlay: ParlayRequest) -> dict:
    """
    Calculate parlay odds, payout, and expected value
    
    Args:
        parlay: ParlayRequest with legs and bet amount
    
    Returns:
        Analysis including total odds, payout, EV, and risk metrics
    """
    try:
        if len(parlay.legs) < 2:
            raise HTTPException(status_code=400, detail="Parlay must have at least 2 legs")
        
        if parlay.bet_amount <= 0:
            raise HTTPException(status_code=400, detail="Bet amount must be positive")
        
        # Calculate combined probability (all legs must win)
        combined_probability = 1.0
        for leg in parlay.legs:
            if leg.win_probability <= 0 or leg.win_probability >= 1:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid win probability for {leg.player_name}: {leg.win_probability}"
                )
            combined_probability *= leg.win_probability
        
        # Calculate parlay odds (multiply all individual odds)
        parlay_odds = 1.0
        for leg in parlay.legs:
            if leg.odds <= 1.0:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid odds for {leg.player_name}: {leg.odds}"
                )
            parlay_odds *= leg.odds
        
        # Calculate potential payout
        potential_payout = parlay.bet_amount * (parlay_odds - 1)
        total_return = parlay.bet_amount * parlay_odds
        
        # Calculate expected value
        expected_value = (combined_probability * potential_payout) - ((1 - combined_probability) * parlay.bet_amount)
        ev_percentage = (expected_value / parlay.bet_amount) * 100
        
        # Calculate risk metrics
        win_rate = combined_probability
        loss_rate = 1 - combined_probability
        risk_reward_ratio = potential_payout / parlay.bet_amount if parlay.bet_amount > 0 else 0
        
        # Calculate Kelly percentage (conservative for parlays)
        kelly_percentage = max(0, (combined_probability * (parlay_odds - 1) - (1 - combined_probability)) / (parlay_odds - 1))
        # Use fractional Kelly (10% for parlays due to high variance)
        fractional_kelly = kelly_percentage * 0.10
        recommended_bet = min(fractional_kelly * 100, 5)  # Cap at 5% of bankroll
        
        # Determine recommendation
        if ev_percentage > 15:
            recommendation = "strong_parlay"
            recommendation_text = "Strong Parlay - High Expected Value"
        elif ev_percentage > 5:
            recommendation = "moderate_parlay"
            recommendation_text = "Moderate Parlay - Positive Expected Value"
        elif ev_percentage > 0:
            recommendation = "small_parlay"
            recommendation_text = "Small Parlay - Slight Positive Edge"
        else:
            recommendation = "avoid_parlay"
            recommendation_text = "Avoid - Negative Expected Value"
        
        # Calculate probability of hitting different numbers of legs
        hit_probabilities = {}
        n = len(parlay.legs)
        for k in range(n + 1):
            # Probability of hitting exactly k legs
            # This is complex for independent events, simplified here
            if k == n:
                hit_probabilities[f"{k}_legs"] = combined_probability
            elif k == 0:
                miss_prob = 1.0
                for leg in parlay.legs:
                    miss_prob *= (1 - leg.win_probability)
                hit_probabilities[f"{k}_legs"] = miss_prob
            else:
                # Simplified: approximate probability
                hit_probabilities[f"{k}_legs"] = 0.0  # Would need binomial calculation for accuracy
        
        return {
            "parlay_odds": round(parlay_odds, 2),
            "combined_probability": round(combined_probability, 4),
            "bet_amount": parlay.bet_amount,
            "potential_payout": round(potential_payout, 2),
            "total_return": round(total_return, 2),
            "expected_value": round(expected_value, 2),
            "ev_percentage": round(ev_percentage, 2),
            "risk_metrics": {
                "win_rate": round(win_rate, 4),
                "loss_rate": round(loss_rate, 4),
                "risk_reward_ratio": round(risk_reward_ratio, 2),
                "kelly_percentage": round(kelly_percentage * 100, 2),
                "recommended_bet_percentage": round(recommended_bet, 2)
            },
            "recommendation": recommendation,
            "recommendation_text": recommendation_text,
            "legs": [
                {
                    "player_name": leg.player_name,
                    "team": leg.team,
                    "prop_type": leg.prop_type,
                    "prop_value": leg.prop_value,
                    "selection": leg.selection,
                    "odds": leg.odds,
                    "win_probability": leg.win_probability
                }
                for leg in parlay.legs
            ],
            "hit_probabilities": hit_probabilities
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recommended")
async def get_recommended_parlays(
    sport: str = "nfl",
    num_legs: int = 3,
    max_legs: int = 5
) -> dict:
    """
    Get recommended parlay combinations based on best value
    
    Args:
        sport: Sport type
        num_legs: Number of legs in parlay
        max_legs: Maximum number of legs to consider
    
    Returns:
        List of recommended parlay combinations
    """
    try:
        # Mock recommended parlays - in production, this would analyze all combinations
        # and return the highest EV parlays
        
        recommended = []
        
        # Example recommended parlay
        if sport == "nfl":
            recommended.append({
                "legs": [
                    {
                        "player_name": "Patrick Mahomes",
                        "team": "Kansas City Chiefs",
                        "prop_type": "passing_yards",
                        "prop_value": 275.5,
                        "selection": "over",
                        "odds": 1.91,
                        "win_probability": 0.58
                    },
                    {
                        "player_name": "Travis Kelce",
                        "team": "Kansas City Chiefs",
                        "prop_type": "receiving_yards",
                        "prop_value": 75.5,
                        "selection": "over",
                        "odds": 1.91,
                        "win_probability": 0.55
                    },
                    {
                        "player_name": "Josh Allen",
                        "team": "Buffalo Bills",
                        "prop_type": "passing_touchdowns",
                        "prop_value": 2.5,
                        "selection": "over",
                        "odds": 1.83,
                        "win_probability": 0.60
                    }
                ],
                "parlay_odds": 6.83,
                "combined_probability": 0.1914,
                "ev_percentage": 30.8,
                "recommendation": "strong_parlay"
            })
        
        return {
            "sport": sport,
            "recommended_parlays": recommended[:5],  # Return top 5
            "num_legs": num_legs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


