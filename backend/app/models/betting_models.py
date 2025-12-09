"""
Professional betting models including Expected Value and Kelly Criterion
"""
from typing import Dict, Optional
from dataclasses import dataclass
import numpy as np


@dataclass
class BetOpportunity:
    """Represents a betting opportunity with calculated metrics"""
    bet_type: str  # "team_win", "player_prop", etc.
    selection: str  # Team name or player name
    odds: float  # Decimal odds
    implied_probability: float
    true_probability: float
    expected_value: float
    kelly_percentage: float
    platform: str
    recommendation: str  # "strong_bet", "moderate_bet", "avoid"


class KellyCriterion:
    """Implements Kelly Criterion for optimal bet sizing"""
    
    @staticmethod
    def calculate_kelly_percentage(
        win_probability: float,
        odds: float,
        kelly_fraction: float = 0.25
    ) -> float:
        """
        Calculate Kelly percentage for bet sizing
        
        Args:
            win_probability: True probability of winning
            odds: Decimal odds
            kelly_fraction: Fraction of Kelly to use (0.25 = quarter Kelly)
        
        Returns:
            Percentage of bankroll to bet
        """
        if odds <= 1.0:
            return 0.0
        
        # Kelly formula: (bp - q) / b
        # where b = odds - 1, p = win prob, q = 1 - p
        b = odds - 1
        p = win_probability
        q = 1 - p
        
        kelly = (b * p - q) / b
        
        # Apply fractional Kelly and ensure non-negative
        fractional_kelly = max(0, kelly * kelly_fraction)
        
        # Cap at 5% of bankroll for safety
        return min(fractional_kelly, 0.05)
    
    @staticmethod
    def calculate_expected_value(
        win_probability: float,
        odds: float
    ) -> float:
        """
        Calculate Expected Value (EV) of a bet
        
        Args:
            win_probability: True probability of winning
            odds: Decimal odds
        
        Returns:
            Expected value as a percentage
        """
        if odds <= 1.0:
            return -1.0
        
        # EV = (win_prob * (odds - 1)) - (lose_prob * 1)
        ev = (win_probability * (odds - 1)) - ((1 - win_probability) * 1)
        return ev


class BettingAnalyzer:
    """Main betting analysis engine"""
    
    def __init__(self, kelly_fraction: float = 0.25):
        self.kelly_fraction = kelly_fraction
        self.kelly_calc = KellyCriterion()
    
    def analyze_bet(
        self,
        true_probability: float,
        odds: float,
        bet_type: str,
        selection: str,
        platform: str
    ) -> BetOpportunity:
        """
        Analyze a betting opportunity
        
        Args:
            true_probability: Model's predicted probability
            odds: Decimal odds from bookmaker
            bet_type: Type of bet
            selection: What is being bet on
            platform: Betting platform name
        
        Returns:
            BetOpportunity with all calculated metrics
        """
        # Calculate implied probability from odds
        implied_prob = 1.0 / odds if odds > 0 else 0.0
        
        # Calculate Expected Value
        ev = self.kelly_calc.calculate_expected_value(true_probability, odds)
        
        # Calculate Kelly percentage
        kelly_pct = self.kelly_calc.calculate_kelly_percentage(
            true_probability, odds, self.kelly_fraction
        )
        
        # Determine recommendation
        if ev > 0.10 and kelly_pct > 0.01:
            recommendation = "strong_bet"
        elif ev > 0.05 and kelly_pct > 0.005:
            recommendation = "moderate_bet"
        elif ev > 0:
            recommendation = "small_bet"
        else:
            recommendation = "avoid"
        
        return BetOpportunity(
            bet_type=bet_type,
            selection=selection,
            odds=odds,
            implied_probability=implied_prob,
            true_probability=true_probability,
            expected_value=ev,
            kelly_percentage=kelly_pct,
            platform=platform,
            recommendation=recommendation
        )
    
    def compare_odds(
        self,
        odds_dict: Dict[str, float],
        true_probability: float,
        bet_type: str,
        selection: str
    ) -> Dict[str, BetOpportunity]:
        """
        Compare odds across multiple platforms
        
        Args:
            odds_dict: Dictionary mapping platform names to odds
            true_probability: Model's predicted probability
            bet_type: Type of bet
            selection: What is being bet on
        
        Returns:
            Dictionary of BetOpportunity objects for each platform
        """
        opportunities = {}
        
        for platform, odds in odds_dict.items():
            opportunities[platform] = self.analyze_bet(
                true_probability, odds, bet_type, selection, platform
            )
        
        return opportunities
    
    def find_best_bet(
        self,
        opportunities: Dict[str, BetOpportunity]
    ) -> Optional[BetOpportunity]:
        """
        Find the best betting opportunity from multiple options
        
        Args:
            opportunities: Dictionary of BetOpportunity objects
        
        Returns:
            Best BetOpportunity or None if no positive EV bets
        """
        positive_ev_bets = {
            k: v for k, v in opportunities.items()
            if v.expected_value > 0
        }
        
        if not positive_ev_bets:
            return None
        
        # Return bet with highest EV
        return max(positive_ev_bets.values(), key=lambda x: x.expected_value)

