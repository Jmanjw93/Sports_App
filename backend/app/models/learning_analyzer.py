"""
Analyzes prediction errors and learns from mistakes
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from collections import defaultdict
from app.models.prediction_tracker import PredictionTracker, StoredPrediction, PredictionOutcome


@dataclass
class LearningInsight:
    """Insight learned from prediction errors"""
    pattern: str
    frequency: int
    impact: float  # How much this pattern affects accuracy
    suggested_adjustment: Dict
    examples: List[str]  # Example prediction IDs where this occurred


class LearningAnalyzer:
    """Analyzes prediction errors and extracts learning patterns"""
    
    def __init__(self, tracker: PredictionTracker):
        self.tracker = tracker
    
    def analyze_prediction_error(self, prediction: StoredPrediction) -> Dict:
        """Analyze why a specific prediction was wrong"""
        if prediction.outcome != PredictionOutcome.INCORRECT:
            return {}
        
        errors = []
        error_severity = 0.0
        contributing_factors = []
        
        # Analyze probability mismatch
        if prediction.predicted_winner == prediction.home_team:
            predicted_prob = prediction.home_win_probability
            actual_winner_prob = prediction.away_win_probability
        else:
            predicted_prob = prediction.away_win_probability
            actual_winner_prob = prediction.home_win_probability
        
        prob_error = abs(predicted_prob - (1 - actual_winner_prob))
        error_severity += prob_error
        
        if prob_error > 0.15:
            errors.append({
                "type": "probability_miscalculation",
                "severity": prob_error,
                "description": f"Predicted {prediction.predicted_winner} with {predicted_prob:.1%} probability, but they lost"
            })
        
        # Analyze confidence vs outcome
        if prediction.confidence > 0.7 and prediction.outcome == PredictionOutcome.INCORRECT:
            errors.append({
                "type": "overconfidence",
                "severity": prediction.confidence,
                "description": f"High confidence ({prediction.confidence:.1%}) but prediction was wrong"
            })
            error_severity += prediction.confidence * 0.3
        
        # Analyze factors that may have been missed
        factors = prediction.factors or {}
        
        # Weather impact analysis
        if factors.get("weather_impact"):
            weather = factors["weather_impact"]
            if weather.get("adjustment") and abs(weather.get("adjustment", 0)) < 0.02:
                errors.append({
                    "type": "weather_underestimated",
                    "severity": 0.2,
                    "description": "Weather impact may have been underestimated"
                })
                contributing_factors.append("weather")
        
        # Injury impact analysis
        if factors.get("injury_impact"):
            injury = factors["injury_impact"]
            home_impact = injury.get("home_injury_impact", 0)
            away_impact = injury.get("away_injury_impact", 0)
            
            if prediction.predicted_winner == prediction.home_team and home_impact > 0.05:
                errors.append({
                    "type": "injury_impact_missed",
                    "severity": home_impact,
                    "description": f"Home team injuries ({home_impact:.1%}) may not have been fully accounted for"
                })
                contributing_factors.append("injuries")
            
            if prediction.predicted_winner == prediction.away_team and away_impact > 0.05:
                errors.append({
                    "type": "injury_impact_missed",
                    "severity": away_impact,
                    "description": f"Away team injuries ({away_impact:.1%}) may not have been fully accounted for"
                })
                contributing_factors.append("injuries")
        
        # Coaching matchup analysis
        if factors.get("coaching_impact"):
            coaching = factors["coaching_impact"]
            if coaching.get("adjustment_factor") and abs(coaching.get("adjustment_factor", 0)) < 0.01:
                errors.append({
                    "type": "coaching_mismatch",
                    "severity": 0.15,
                    "description": "Coaching matchup impact may have been underestimated"
                })
                contributing_factors.append("coaching")
        
        # Mental health analysis
        if factors.get("mental_health_impact"):
            mh = factors["mental_health_impact"]
            adjustment = mh.get("adjustment", 0)
            if abs(adjustment) < 0.01:
                errors.append({
                    "type": "mental_health_underestimated",
                    "severity": 0.1,
                    "description": "Mental health factors may have been underestimated"
                })
                contributing_factors.append("mental_health")
        
        return {
            "prediction_id": prediction.prediction_id,
            "error_severity": min(error_severity, 1.0),
            "errors": errors,
            "contributing_factors": contributing_factors,
            "suggested_adjustments": self._generate_adjustments(errors, contributing_factors)
        }
    
    def _generate_adjustments(self, errors: List[Dict], factors: List[str]) -> Dict:
        """Generate suggested adjustments based on errors"""
        adjustments = {}
        
        for error in errors:
            error_type = error["type"]
            severity = error.get("severity", 0.1)
            
            if error_type == "weather_underestimated":
                adjustments["weather_weight"] = min(0.20, 0.15 + severity * 0.1)
            elif error_type == "injury_impact_missed":
                adjustments["injury_weight"] = min(0.25, 0.15 + severity * 0.2)
            elif error_type == "coaching_mismatch":
                adjustments["coaching_weight"] = min(0.20, 0.10 + severity * 0.2)
            elif error_type == "mental_health_underestimated":
                adjustments["mental_health_weight"] = min(0.18, 0.12 + severity * 0.1)
            elif error_type == "overconfidence":
                adjustments["confidence_penalty"] = severity * 0.1
        
        return adjustments
    
    def extract_learning_patterns(self, sport: Optional[str] = None) -> List[LearningInsight]:
        """Extract common patterns from prediction errors"""
        predictions = [p for p in self.tracker.predictions.values() 
                      if p.outcome == PredictionOutcome.INCORRECT]
        
        if sport:
            predictions = [p for p in predictions if p.sport == sport]
        
        if not predictions:
            return []
        
        # Analyze error patterns
        error_patterns = defaultdict(lambda: {"count": 0, "total_severity": 0.0, "examples": []})
        
        for prediction in predictions:
            analysis = self.analyze_prediction_error(prediction)
            
            for error in analysis.get("errors", []):
                error_type = error["type"]
                error_patterns[error_type]["count"] += 1
                error_patterns[error_type]["total_severity"] += error.get("severity", 0.1)
                if len(error_patterns[error_type]["examples"]) < 5:
                    error_patterns[error_type]["examples"].append(prediction.prediction_id)
        
        # Convert to LearningInsight objects
        insights = []
        total_errors = len(predictions)
        
        for pattern, data in error_patterns.items():
            frequency = data["count"] / total_errors if total_errors > 0 else 0
            avg_impact = data["total_severity"] / data["count"] if data["count"] > 0 else 0
            
            # Generate suggested adjustments
            suggested_adjustment = {}
            if "weather" in pattern.lower():
                suggested_adjustment["weather_weight"] = min(0.25, 0.15 + avg_impact * 0.2)
            elif "injury" in pattern.lower():
                suggested_adjustment["injury_weight"] = min(0.30, 0.15 + avg_impact * 0.3)
            elif "coaching" in pattern.lower():
                suggested_adjustment["coaching_weight"] = min(0.25, 0.10 + avg_impact * 0.3)
            elif "mental" in pattern.lower():
                suggested_adjustment["mental_health_weight"] = min(0.20, 0.12 + avg_impact * 0.15)
            elif "confidence" in pattern.lower():
                suggested_adjustment["confidence_penalty"] = avg_impact * 0.15
            
            insights.append(LearningInsight(
                pattern=pattern,
                frequency=frequency,
                impact=avg_impact,
                suggested_adjustment=suggested_adjustment,
                examples=data["examples"]
            ))
        
        # Sort by impact
        insights.sort(key=lambda x: x.impact * x.frequency, reverse=True)
        return insights
    
    def get_improvement_recommendations(self, sport: Optional[str] = None) -> Dict:
        """Get recommendations for improving predictions"""
        patterns = self.extract_learning_patterns(sport)
        stats = self.tracker.get_accuracy_stats(sport)
        
        recommendations = []
        
        for insight in patterns[:5]:  # Top 5 patterns
            if insight.frequency > 0.1:  # Pattern occurs in >10% of errors
                recommendations.append({
                    "pattern": insight.pattern,
                    "frequency": f"{insight.frequency:.1%}",
                    "impact": f"{insight.impact:.1%}",
                    "adjustment": insight.suggested_adjustment,
                    "description": self._get_pattern_description(insight.pattern)
                })
        
        return {
            "current_accuracy": stats["accuracy"],
            "total_predictions": stats["total"],
            "recommendations": recommendations,
            "top_errors": [p.pattern for p in patterns[:3]]
        }
    
    def _get_pattern_description(self, pattern: str) -> str:
        """Get human-readable description of error pattern"""
        descriptions = {
            "weather_underestimated": "Weather conditions are being underestimated. Consider increasing weather impact weight.",
            "injury_impact_missed": "Injury impacts are not being fully accounted for. Increase injury weight in calculations.",
            "coaching_mismatch": "Coaching matchup factors need more weight in predictions.",
            "mental_health_underestimated": "Mental health factors should have greater influence on predictions.",
            "overconfidence": "Model is overconfident. Apply confidence penalties for high-confidence predictions.",
            "probability_miscalculation": "Base probability calculations need adjustment."
        }
        return descriptions.get(pattern, f"Pattern: {pattern}")




