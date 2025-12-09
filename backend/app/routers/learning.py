"""
API routes for prediction learning and feedback
"""
from fastapi import APIRouter, HTTPException
from typing import Optional, Dict, List
from datetime import datetime
from app.models.prediction_tracker import PredictionTracker, PredictionOutcome
from app.models.learning_analyzer import LearningAnalyzer
from pydantic import BaseModel

router = APIRouter()

# Initialize tracker and analyzer
tracker = PredictionTracker()
analyzer = LearningAnalyzer(tracker)


class GameResult(BaseModel):
    """Game result submission"""
    game_id: str
    actual_winner: str
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    game_date: Optional[str] = None


@router.post("/submit-result")
async def submit_game_result(result: GameResult) -> dict:
    """
    Submit actual game result to track prediction accuracy
    
    Args:
        result: GameResult with actual winner and score
    
    Returns:
        Analysis of prediction accuracy
    """
    try:
        # Find predictions for this game
        predictions = tracker.get_predictions_by_game(result.game_id)
        
        if not predictions:
            raise HTTPException(
                status_code=404,
                detail=f"No predictions found for game {result.game_id}"
            )
        
        # Record outcomes for all predictions
        score = None
        if result.home_score is not None and result.away_score is not None:
            score = {
                "home": result.home_score,
                "away": result.away_score
            }
        
        updated_predictions = []
        for prediction in predictions:
            tracker.record_outcome(
                prediction.prediction_id,
                result.actual_winner,
                score
            )
            
            # Analyze the error if prediction was wrong
            if prediction.outcome == PredictionOutcome.INCORRECT:
                error_analysis = analyzer.analyze_prediction_error(prediction)
                prediction.error_analysis = error_analysis
                tracker._save_predictions()
            
            updated_predictions.append({
                "prediction_id": prediction.prediction_id,
                "predicted_winner": prediction.predicted_winner,
                "actual_winner": result.actual_winner,
                "outcome": prediction.outcome.value,
                "error_analysis": prediction.error_analysis
            })
        
        return {
            "game_id": result.game_id,
            "actual_winner": result.actual_winner,
            "predictions_updated": len(updated_predictions),
            "results": updated_predictions
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/accuracy")
async def get_accuracy_stats(sport: Optional[str] = None) -> dict:
    """
    Get prediction accuracy statistics
    
    Args:
        sport: Optional sport filter
    
    Returns:
        Accuracy statistics
    """
    try:
        stats = tracker.get_accuracy_stats(sport)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/insights")
async def get_learning_insights(sport: Optional[str] = None) -> dict:
    """
    Get learning insights from prediction errors
    
    Args:
        sport: Optional sport filter
    
    Returns:
        Learning insights and recommendations
    """
    try:
        recommendations = analyzer.get_improvement_recommendations(sport)
        patterns = analyzer.extract_learning_patterns(sport)
        
        return {
            "recommendations": recommendations,
            "error_patterns": [
                {
                    "pattern": p.pattern,
                    "frequency": f"{p.frequency:.1%}",
                    "impact": f"{p.impact:.1%}",
                    "suggested_adjustment": p.suggested_adjustment
                }
                for p in patterns
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/predictions")
async def get_predictions(
    game_id: Optional[str] = None,
    sport: Optional[str] = None,
    limit: int = 50
) -> dict:
    """
    Get stored predictions
    
    Args:
        game_id: Optional game ID filter
        sport: Optional sport filter
        limit: Maximum number of predictions to return
    
    Returns:
        List of predictions
    """
    try:
        if game_id:
            predictions = tracker.get_predictions_by_game(game_id)
        else:
            predictions = tracker.get_recent_predictions(limit)
        
        if sport:
            predictions = [p for p in predictions if p.sport == sport]
        
        return {
            "predictions": [
                {
                    "prediction_id": p.prediction_id,
                    "game_id": p.game_id,
                    "sport": p.sport,
                    "home_team": p.home_team,
                    "away_team": p.away_team,
                    "predicted_winner": p.predicted_winner,
                    "actual_winner": p.actual_winner,
                    "home_win_probability": p.home_win_probability,
                    "away_win_probability": p.away_win_probability,
                    "confidence": p.confidence,
                    "outcome": p.outcome.value,
                    "prediction_date": p.prediction_date.isoformat() if p.prediction_date else None,
                    "error_analysis": p.error_analysis
                }
                for p in predictions
            ],
            "total": len(predictions)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/error-analysis/{prediction_id}")
async def get_error_analysis(prediction_id: str) -> dict:
    """
    Get detailed error analysis for a specific prediction
    
    Args:
        prediction_id: Prediction ID
    
    Returns:
        Detailed error analysis
    """
    try:
        prediction = tracker.get_prediction(prediction_id)
        if not prediction:
            raise HTTPException(status_code=404, detail="Prediction not found")
        
        if prediction.outcome != PredictionOutcome.INCORRECT:
            return {
                "prediction_id": prediction_id,
                "outcome": prediction.outcome.value,
                "message": "Prediction was correct, no error analysis available"
            }
        
        analysis = analyzer.analyze_prediction_error(prediction)
        return {
            "prediction_id": prediction_id,
            "game_id": prediction.game_id,
            "predicted_winner": prediction.predicted_winner,
            "actual_winner": prediction.actual_winner,
            "error_analysis": analysis
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

