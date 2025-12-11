"""
Adaptive predictor that learns from past mistakes
"""
from typing import Dict, Optional
from app.models.prediction_tracker import PredictionTracker
from app.models.learning_analyzer import LearningAnalyzer


class AdaptivePredictor:
    """Adjusts prediction weights based on learning from past errors"""
    
    def __init__(self, tracker: PredictionTracker):
        self.tracker = tracker
        self.analyzer = LearningAnalyzer(tracker)
        self.base_weights = {
            "weather": 0.15,
            "injury": 0.15,
            "coaching": 0.10,
            "mental_health": 0.12,
            "home_advantage": 0.03
        }
    
    def get_adjusted_weights(self, sport: Optional[str] = None) -> Dict[str, float]:
        """
        Get adjusted weights based on learning from past errors
        
        Args:
            sport: Optional sport filter
        
        Returns:
            Dictionary of adjusted weights
        """
        # Get learning insights
        insights = self.analyzer.extract_learning_patterns(sport)
        
        # Start with base weights
        adjusted_weights = self.base_weights.copy()
        
        # Apply adjustments based on error patterns
        for insight in insights:
            if insight.frequency > 0.1:  # Only adjust if pattern occurs frequently
                adjustments = insight.suggested_adjustment
                
                if "weather_weight" in adjustments:
                    adjusted_weights["weather"] = adjustments["weather_weight"]
                if "injury_weight" in adjustments:
                    adjusted_weights["injury"] = adjustments["injury_weight"]
                if "coaching_weight" in adjustments:
                    adjusted_weights["coaching"] = adjustments["coaching_weight"]
                if "mental_health_weight" in adjustments:
                    adjusted_weights["mental_health"] = adjustments["mental_health_weight"]
        
        return adjusted_weights
    
    def get_confidence_adjustment(self, base_confidence: float, sport: Optional[str] = None) -> float:
        """
        Adjust confidence based on historical accuracy
        
        Args:
            base_confidence: Base confidence from prediction
            sport: Optional sport filter
        
        Returns:
            Adjusted confidence
        """
        stats = self.tracker.get_accuracy_stats(sport)
        
        if stats["total"] < 10:  # Not enough data
            return base_confidence
        
        accuracy = stats["accuracy"]
        
        # If accuracy is low, reduce confidence
        if accuracy < 0.5:
            return base_confidence * 0.8
        elif accuracy < 0.6:
            return base_confidence * 0.9
        # If accuracy is high, slightly increase confidence
        elif accuracy > 0.75:
            return min(1.0, base_confidence * 1.05)
        
        return base_confidence




