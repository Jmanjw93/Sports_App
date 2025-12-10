"""
Prediction tracking and outcome storage
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum
import json
import os


class PredictionOutcome(Enum):
    """Actual outcome of a prediction"""
    CORRECT = "correct"
    INCORRECT = "incorrect"
    PENDING = "pending"


@dataclass
class StoredPrediction:
    """Stored prediction with metadata"""
    prediction_id: str
    game_id: str
    sport: str
    home_team: str
    away_team: str
    predicted_winner: str
    actual_winner: Optional[str] = None
    home_win_probability: float = 0.0
    away_win_probability: float = 0.0
    confidence: float = 0.0
    game_date: Optional[datetime] = None
    prediction_date: datetime = field(default_factory=datetime.now)
    outcome: PredictionOutcome = PredictionOutcome.PENDING
    factors: Dict = field(default_factory=dict)  # Weather, injuries, coaching, etc.
    score: Optional[Dict] = None  # Actual game score
    error_analysis: Optional[Dict] = None  # Analysis of why prediction was wrong
    locked: bool = False  # Whether this prediction was manually locked by user
    locked_date: Optional[datetime] = None  # When the prediction was locked
    full_prediction_data: Optional[Dict] = None  # Full prediction data snapshot when locked


@dataclass
class PredictionError:
    """Analysis of a prediction error"""
    prediction_id: str
    error_type: str  # e.g., "weather_underestimated", "injury_impact_missed", "coaching_mismatch"
    error_severity: float  # 0.0 to 1.0
    contributing_factors: List[str]
    suggested_adjustments: Dict


class PredictionTracker:
    """Tracks predictions and their outcomes"""
    
    def __init__(self, storage_path: str = "data/predictions.json"):
        self.storage_path = storage_path
        self.predictions: Dict[str, StoredPrediction] = {}
        self._load_predictions()
    
    def _load_predictions(self):
        """Load predictions from storage"""
        if os.path.exists(self.storage_path):
            try:
                os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    for pred_id, pred_data in data.items():
                        # Convert datetime strings back to datetime objects
                        if 'prediction_date' in pred_data and pred_data['prediction_date']:
                            pred_data['prediction_date'] = datetime.fromisoformat(pred_data['prediction_date'])
                        if 'game_date' in pred_data and pred_data['game_date']:
                            pred_data['game_date'] = datetime.fromisoformat(pred_data['game_date'])
                        if 'locked_date' in pred_data and pred_data['locked_date']:
                            pred_data['locked_date'] = datetime.fromisoformat(pred_data['locked_date'])
                        if 'outcome' in pred_data:
                            pred_data['outcome'] = PredictionOutcome(pred_data['outcome'])
                        self.predictions[pred_id] = StoredPrediction(**pred_data)
            except Exception as e:
                print(f"Error loading predictions: {e}")
                self.predictions = {}
    
    def _save_predictions(self):
        """Save predictions to storage"""
        try:
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            data = {}
            for pred_id, pred in self.predictions.items():
                pred_dict = pred.__dict__.copy()
                # Convert datetime objects to ISO strings
                if pred_dict.get('prediction_date'):
                    pred_dict['prediction_date'] = pred_dict['prediction_date'].isoformat()
                if pred_dict.get('game_date'):
                    pred_dict['game_date'] = pred_dict['game_date'].isoformat()
                if pred_dict.get('locked_date'):
                    pred_dict['locked_date'] = pred_dict['locked_date'].isoformat()
                if pred_dict.get('outcome'):
                    pred_dict['outcome'] = pred_dict['outcome'].value
                data[pred_id] = pred_dict
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving predictions: {e}")
    
    def store_prediction(
        self,
        game_id: str,
        sport: str,
        home_team: str,
        away_team: str,
        predicted_winner: str,
        home_win_probability: float,
        away_win_probability: float,
        confidence: float,
        factors: Dict,
        game_date: Optional[datetime] = None
    ) -> str:
        """Store a new prediction"""
        prediction_id = f"{game_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        prediction = StoredPrediction(
            prediction_id=prediction_id,
            game_id=game_id,
            sport=sport,
            home_team=home_team,
            away_team=away_team,
            predicted_winner=predicted_winner,
            home_win_probability=home_win_probability,
            away_win_probability=away_win_probability,
            confidence=confidence,
            game_date=game_date,
            factors=factors
        )
        
        self.predictions[prediction_id] = prediction
        self._save_predictions()
        return prediction_id
    
    def record_outcome(
        self,
        prediction_id: str,
        actual_winner: str,
        score: Optional[Dict] = None
    ):
        """Record the actual outcome of a prediction"""
        if prediction_id not in self.predictions:
            raise ValueError(f"Prediction {prediction_id} not found")
        
        prediction = self.predictions[prediction_id]
        prediction.actual_winner = actual_winner
        prediction.score = score
        prediction.outcome = PredictionOutcome.CORRECT if actual_winner == prediction.predicted_winner else PredictionOutcome.INCORRECT
        
        self._save_predictions()
        return prediction
    
    def get_prediction(self, prediction_id: str) -> Optional[StoredPrediction]:
        """Get a stored prediction"""
        return self.predictions.get(prediction_id)
    
    def get_predictions_by_game(self, game_id: str) -> List[StoredPrediction]:
        """Get all predictions for a specific game"""
        return [p for p in self.predictions.values() if p.game_id == game_id]
    
    def get_recent_predictions(self, limit: int = 100) -> List[StoredPrediction]:
        """Get recent predictions"""
        sorted_predictions = sorted(
            self.predictions.values(),
            key=lambda x: x.prediction_date,
            reverse=True
        )
        return sorted_predictions[:limit]
    
    def get_accuracy_stats(self, sport: Optional[str] = None) -> Dict:
        """Get accuracy statistics"""
        predictions = [p for p in self.predictions.values() if p.outcome != PredictionOutcome.PENDING]
        if sport:
            predictions = [p for p in predictions if p.sport == sport]
        
        if not predictions:
            return {
                "total": 0,
                "correct": 0,
                "incorrect": 0,
                "accuracy": 0.0
            }
        
        correct = sum(1 for p in predictions if p.outcome == PredictionOutcome.CORRECT)
        incorrect = sum(1 for p in predictions if p.outcome == PredictionOutcome.INCORRECT)
        
        return {
            "total": len(predictions),
            "correct": correct,
            "incorrect": incorrect,
            "accuracy": correct / len(predictions) if predictions else 0.0,
            "pending": sum(1 for p in self.predictions.values() if p.outcome == PredictionOutcome.PENDING)
        }
    
    def lock_prediction(
        self,
        game_id: str,
        sport: str,
        home_team: str,
        away_team: str,
        predicted_winner: str,
        home_win_probability: float,
        away_win_probability: float,
        confidence: float,
        factors: Dict,
        full_prediction_data: Dict,
        game_date: Optional[datetime] = None
    ) -> str:
        """Lock a prediction for future analysis"""
        prediction_id = f"{game_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        prediction = StoredPrediction(
            prediction_id=prediction_id,
            game_id=game_id,
            sport=sport,
            home_team=home_team,
            away_team=away_team,
            predicted_winner=predicted_winner,
            home_win_probability=home_win_probability,
            away_win_probability=away_win_probability,
            confidence=confidence,
            game_date=game_date,
            factors=factors,
            locked=True,
            locked_date=datetime.now(),
            full_prediction_data=full_prediction_data
        )
        
        self.predictions[prediction_id] = prediction
        self._save_predictions()
        return prediction_id
    
    def get_locked_predictions(self, include_resolved: bool = True) -> List[StoredPrediction]:
        """Get all locked predictions"""
        locked = [p for p in self.predictions.values() if p.locked]
        if not include_resolved:
            locked = [p for p in locked if p.outcome == PredictionOutcome.PENDING]
        return sorted(locked, key=lambda x: x.locked_date or x.prediction_date, reverse=True)
    
    def analyze_prediction_accuracy(self, prediction_id: str) -> Dict:
        """Analyze why a prediction was correct or incorrect"""
        prediction = self.get_prediction(prediction_id)
        if not prediction:
            return {"error": "Prediction not found"}
        
        if prediction.outcome == PredictionOutcome.PENDING:
            return {"error": "Prediction outcome not yet recorded"}
        
        analysis = {
            "prediction_id": prediction_id,
            "was_correct": prediction.outcome == PredictionOutcome.CORRECT,
            "predicted_winner": prediction.predicted_winner,
            "actual_winner": prediction.actual_winner,
            "predicted_probabilities": {
                "home": prediction.home_win_probability,
                "away": prediction.away_win_probability
            },
            "confidence": prediction.confidence,
            "factors_analysis": {}
        }
        
        # Analyze factors that contributed to the outcome
        if prediction.factors:
            # Weather impact analysis
            if "weather" in prediction.factors:
                weather = prediction.factors.get("weather", {})
                analysis["factors_analysis"]["weather"] = {
                    "had_impact": bool(weather),
                    "description": weather.get("description", "No significant weather impact")
                }
            
            # Injury impact analysis
            if "injuries" in prediction.factors:
                injuries = prediction.factors.get("injuries", {})
                analysis["factors_analysis"]["injuries"] = {
                    "home_impact": injuries.get("home_injury_impact", 0),
                    "away_impact": injuries.get("away_injury_impact", 0),
                    "adjustment": injuries.get("adjustment", 0)
                }
            
            # Coaching impact analysis
            if "coaching" in prediction.factors:
                coaching = prediction.factors.get("coaching", {})
                analysis["factors_analysis"]["coaching"] = {
                    "adjustment": coaching.get("adjustment_factor", 0),
                    "insight": coaching.get("key_insight", "")
                }
            
            # Mental health impact analysis
            if "mental_health" in prediction.factors:
                mental_health = prediction.factors.get("mental_health", {})
                analysis["factors_analysis"]["mental_health"] = {
                    "net_adjustment": mental_health.get("net_adjustment", 0),
                    "summary": mental_health.get("summary", "")
                }
        
        # Determine what went right or wrong
        if prediction.outcome == PredictionOutcome.CORRECT:
            analysis["success_factors"] = [
                "Prediction correctly identified the winner",
                f"Confidence level: {prediction.confidence:.0%}",
                "Key factors aligned with actual outcome"
            ]
        else:
            analysis["error_factors"] = [
                f"Predicted {prediction.predicted_winner} but {prediction.actual_winner} won",
                f"Confidence was {prediction.confidence:.0%} but prediction was incorrect",
                "Key factors may have been misweighted or changed"
            ]
        
        return analysis

