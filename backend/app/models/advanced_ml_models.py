"""
Advanced ML models for sports predictions using scikit-learn and XGBoost
"""
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import xgboost as xgb
import pickle
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class AdvancedMLPredictor:
    """
    Advanced ML-based predictor using ensemble methods
    """
    
    def __init__(self, model_dir: str = "models"):
        self.model_dir = model_dir
        os.makedirs(model_dir, exist_ok=True)
        
        # Initialize models
        self.models = {}
        self.scalers = {}
        self.feature_names = {}
        
        # Model types
        self.model_types = {
            'random_forest': RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10),
            'gradient_boosting': GradientBoostingClassifier(n_estimators=100, random_state=42, max_depth=5),
            'xgboost': xgb.XGBClassifier(n_estimators=100, random_state=42, max_depth=5, learning_rate=0.1),
            'logistic': LogisticRegression(random_state=42, max_iter=1000)
        }
    
    def _extract_features(
        self,
        home_stats: Dict,
        away_stats: Dict,
        weather_data: Optional[Dict] = None,
        injury_data: Optional[Dict] = None
    ) -> np.ndarray:
        """
        Extract features from game data
        
        Args:
            home_stats: Home team statistics
            away_stats: Away team statistics
            weather_data: Optional weather data
            injury_data: Optional injury data
        
        Returns:
            Feature vector as numpy array
        """
        features = []
        
        # Team strength features
        features.extend([
            home_stats.get("win_rate", 0.5),
            home_stats.get("points_per_game", 0) / 100.0,  # Normalized
            home_stats.get("points_allowed_per_game", 0) / 100.0,  # Normalized
            home_stats.get("recent_form", 0.5),
            home_stats.get("home_record", {}).get("wins", 0) / 10.0,  # Normalized
            home_stats.get("home_record", {}).get("losses", 0) / 10.0,  # Normalized
        ])
        
        features.extend([
            away_stats.get("win_rate", 0.5),
            away_stats.get("points_per_game", 0) / 100.0,
            away_stats.get("points_allowed_per_game", 0) / 100.0,
            away_stats.get("recent_form", 0.5),
            away_stats.get("away_record", {}).get("wins", 0) / 10.0,
            away_stats.get("away_record", {}).get("losses", 0) / 10.0,
        ])
        
        # Differential features
        features.extend([
            home_stats.get("win_rate", 0.5) - away_stats.get("win_rate", 0.5),
            (home_stats.get("points_per_game", 0) - away_stats.get("points_allowed_per_game", 0)) / 100.0,
            (away_stats.get("points_per_game", 0) - home_stats.get("points_allowed_per_game", 0)) / 100.0,
            home_stats.get("recent_form", 0.5) - away_stats.get("recent_form", 0.5),
        ])
        
        # Weather features (if available)
        if weather_data:
            temp = weather_data.get("temp", 70)
            wind = weather_data.get("wind_speed", 0)
            precip = weather_data.get("precipitation", 0)
            
            features.extend([
                temp / 100.0,  # Normalized
                wind / 50.0,  # Normalized
                precip / 10.0,  # Normalized
                1 if temp < 32 else 0,  # Cold indicator
                1 if wind > 20 else 0,  # High wind indicator
                1 if precip > 0 else 0,  # Precipitation indicator
            ])
        else:
            features.extend([0.7, 0.0, 0.0, 0, 0, 0])  # Default values
        
        # Injury features (if available)
        if injury_data:
            home_injuries = injury_data.get("home_injuries", {})
            away_injuries = injury_data.get("away_injuries", {})
            
            features.extend([
                home_injuries.get("key_players_out", 0) / 5.0,  # Normalized
                home_injuries.get("total_injuries", 0) / 10.0,  # Normalized
                away_injuries.get("key_players_out", 0) / 5.0,
                away_injuries.get("total_injuries", 0) / 10.0,
            ])
        else:
            features.extend([0.0, 0.0, 0.0, 0.0])
        
        # Home advantage
        features.append(0.03)  # Standard home advantage
        
        return np.array(features).reshape(1, -1)
    
    def predict_game_ml(
        self,
        home_team: str,
        away_team: str,
        home_stats: Dict,
        away_stats: Dict,
        sport: str = "nfl",
        weather_data: Optional[Dict] = None,
        injury_data: Optional[Dict] = None,
        model_type: str = "ensemble"
    ) -> Dict:
        """
        Predict game outcome using ML models
        
        Args:
            home_team: Home team name
            away_team: Away team name
            home_stats: Home team statistics
            away_stats: Away team statistics
            sport: Sport type
            weather_data: Optional weather data
            injury_data: Optional injury data
            model_type: Type of model to use ('random_forest', 'gradient_boosting', 'xgboost', 'logistic', 'ensemble')
        
        Returns:
            Prediction dictionary with probabilities and confidence
        """
        # Extract features
        features = self._extract_features(home_stats, away_stats, weather_data, injury_data)
        
        # Load or create model for this sport
        model_key = f"{sport}_{model_type}"
        
        if model_key not in self.models:
            # Train a model if it doesn't exist (using synthetic data for now)
            self._train_model(sport, model_type)
        
        # Get predictions
        if model_type == "ensemble":
            # Use ensemble of all models
            predictions = []
            for mt in ['random_forest', 'gradient_boosting', 'xgboost']:
                mt_key = f"{sport}_{mt}"
                if mt_key in self.models:
                    model = self.models[mt_key]
                    scaler = self.scalers.get(mt_key)
                    
                    if scaler:
                        features_scaled = scaler.transform(features)
                    else:
                        features_scaled = features
                    
                    prob = model.predict_proba(features_scaled)[0]
                    predictions.append(prob[1])  # Probability of home win
            
            if predictions:
                home_win_prob = np.mean(predictions)
            else:
                # Fallback to simple calculation
                home_win_prob = self._fallback_prediction(home_stats, away_stats)
        else:
            model = self.models[model_key]
            scaler = self.scalers.get(model_key)
            
            if scaler:
                features_scaled = scaler.transform(features)
            else:
                features_scaled = features
            
            prob = model.predict_proba(features_scaled)[0]
            home_win_prob = prob[1]  # Probability of home win
        
        # Calculate confidence based on prediction strength
        confidence = abs(home_win_prob - 0.5) * 2  # Convert to 0-1 scale
        
        # Determine winner
        predicted_winner = home_team if home_win_prob > 0.5 else away_team
        
        return {
            "predicted_winner": predicted_winner,
            "home_win_probability": float(home_win_prob),
            "away_win_probability": float(1 - home_win_prob),
            "confidence": float(confidence),
            "model_type": model_type,
            "features_used": len(features[0])
        }
    
    def _train_model(self, sport: str, model_type: str):
        """
        Train a model for a specific sport (using synthetic data)
        In production, this would use historical game data
        """
        # Generate synthetic training data
        # In production, load from database
        n_samples = 1000
        n_features = 28  # Match feature count
        
        X = np.random.rand(n_samples, n_features)
        # Create realistic target distribution
        y = (X[:, 0] + X[:, 1] - X[:, 6] - X[:, 7] + np.random.rand(n_samples) * 0.2 > 0).astype(int)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        if model_type == "ensemble":
            # Train all models
            for mt in ['random_forest', 'gradient_boosting', 'xgboost']:
                self._train_single_model(sport, mt, X_train_scaled, y_train, scaler)
        else:
            self._train_single_model(sport, model_type, X_train_scaled, y_train, scaler)
    
    def _train_single_model(self, sport: str, model_type: str, X_train: np.ndarray, y_train: np.ndarray, scaler: StandardScaler):
        """Train a single model"""
        model_key = f"{sport}_{model_type}"
        
        if model_type not in self.model_types:
            return
        
        model = self.model_types[model_type]
        model.fit(X_train, y_train)
        
        self.models[model_key] = model
        self.scalers[model_key] = scaler
        
        # Save model
        model_path = os.path.join(self.model_dir, f"{model_key}.pkl")
        scaler_path = os.path.join(self.model_dir, f"{model_key}_scaler.pkl")
        
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        with open(scaler_path, 'wb') as f:
            pickle.dump(scaler, f)
    
    def _fallback_prediction(self, home_stats: Dict, away_stats: Dict) -> float:
        """Fallback prediction using simple heuristics"""
        home_strength = (
            home_stats.get("win_rate", 0.5) * 0.4 +
            (home_stats.get("points_per_game", 0) / 100) * 0.3 +
            (1 - home_stats.get("points_allowed_per_game", 0) / 100) * 0.2 +
            home_stats.get("recent_form", 0.5) * 0.1
        )
        
        away_strength = (
            away_stats.get("win_rate", 0.5) * 0.4 +
            (away_stats.get("points_per_game", 0) / 100) * 0.3 +
            (1 - away_stats.get("points_allowed_per_game", 0) / 100) * 0.2 +
            away_stats.get("recent_form", 0.5) * 0.1
        )
        
        home_strength += 0.03  # Home advantage
        
        total = home_strength + away_strength
        return home_strength / total if total > 0 else 0.5
    
    def load_model(self, sport: str, model_type: str) -> bool:
        """Load a pre-trained model from disk"""
        model_key = f"{sport}_{model_type}"
        model_path = os.path.join(self.model_dir, f"{model_key}.pkl")
        scaler_path = os.path.join(self.model_dir, f"{model_key}_scaler.pkl")
        
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            try:
                with open(model_path, 'rb') as f:
                    self.models[model_key] = pickle.load(f)
                with open(scaler_path, 'rb') as f:
                    self.scalers[model_key] = pickle.load(f)
                return True
            except Exception as e:
                print(f"Error loading model {model_key}: {e}")
                return False
        return False


class PlayerPropMLPredictor:
    """
    ML-based player prop predictor
    """
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
    
    def predict_player_prop_ml(
        self,
        player_name: str,
        prop_type: str,
        player_stats: Dict,
        opponent_stats: Dict,
        historical_avg: float,
        line: Optional[float] = None
    ) -> Dict:
        """
        Predict player prop using ML
        
        Args:
            player_name: Player name
            prop_type: Type of prop (points, yards, etc.)
            player_stats: Player statistics
            opponent_stats: Opponent defensive statistics
            historical_avg: Historical average
            line: Betting line
        
        Returns:
            Prediction dictionary
        """
        # Extract features
        features = self._extract_player_features(
            player_stats, opponent_stats, historical_avg, prop_type
        )
        
        # Simple regression-based prediction
        # In production, use trained regression models
        base_prediction = player_stats.get(f"{prop_type}_avg", historical_avg)
        
        # Matchup adjustment
        matchup_factor = self._calculate_matchup_factor(
            player_stats, opponent_stats, prop_type
        )
        
        predicted_value = base_prediction * matchup_factor
        
        # Calculate probabilities if line provided
        if line:
            # Use normal distribution approximation
            std_dev = predicted_value * 0.15
            z_score = (line - predicted_value) / std_dev if std_dev > 0 else 0
            
            # Convert z-score to probability (simplified without scipy)
            # Using error function approximation
            import math
            # Approximate normal CDF
            if z_score < -6:
                over_prob = 1.0
            elif z_score > 6:
                over_prob = 0.0
            else:
                # Approximation of 1 - CDF(z) = CDF(-z)
                over_prob = 0.5 * (1 + math.erf(-z_score / math.sqrt(2)))
        else:
            over_prob = 0.5
        
        confidence = min(0.95, player_stats.get("consistency", 0.7) * 0.9)
        
        return {
            "player_name": player_name,
            "prop_type": prop_type,
            "predicted_value": float(predicted_value),
            "over_probability": float(over_prob),
            "under_probability": float(1 - over_prob),
            "confidence": float(confidence),
            "historical_avg": float(historical_avg),
            "matchup_factor": float(matchup_factor)
        }
    
    def _extract_player_features(
        self,
        player_stats: Dict,
        opponent_stats: Dict,
        historical_avg: float,
        prop_type: str
    ) -> np.ndarray:
        """Extract features for player prop prediction"""
        features = [
            player_stats.get(f"{prop_type}_avg", historical_avg) / 100.0,  # Normalized
            player_stats.get("consistency", 0.7),
            player_stats.get("recent_trend", 0.0),
            opponent_stats.get(f"defense_vs_{prop_type}", 0.5),
            historical_avg / 100.0,  # Normalized
        ]
        return np.array(features)
    
    def _calculate_matchup_factor(
        self,
        player_stats: Dict,
        opponent_stats: Dict,
        prop_type: str
    ) -> float:
        """Calculate matchup factor"""
        opponent_defense = opponent_stats.get(f"defense_vs_{prop_type}", 0.5)
        matchup_factor = 1.0 + (0.5 - opponent_defense) * 0.3
        return max(0.7, min(1.3, matchup_factor))

