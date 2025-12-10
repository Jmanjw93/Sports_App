"""
Advanced statistical utilities for sports analytics
Implements best practices for probability, averages, and uncertainty quantification
"""
import numpy as np
from typing import List, Dict, Tuple, Optional
from scipy import stats
from datetime import datetime, timedelta
import math


class StatisticalUtils:
    """
    Advanced statistical methods for sports analytics
    """
    
    @staticmethod
    def time_weighted_average(
        values: List[float],
        dates: List[datetime],
        half_life_days: float = 30.0,
        reference_date: Optional[datetime] = None
    ) -> Tuple[float, float]:
        """
        Calculate time-weighted average where recent values have more weight
        
        Uses exponential decay: weight = exp(-days_ago / half_life)
        
        Args:
            values: List of values to average
            dates: List of corresponding dates
            half_life_days: Number of days for weight to decay by 50%
            reference_date: Date to calculate weights from (default: most recent date)
        
        Returns:
            Tuple of (weighted_average, effective_sample_size)
        """
        if not values or len(values) != len(dates):
            return 0.0, 0.0
        
        if reference_date is None:
            reference_date = max(dates)
        
        # Calculate weights using exponential decay
        weights = []
        for date in dates:
            days_ago = (reference_date - date).days
            weight = math.exp(-days_ago / half_life_days)
            weights.append(weight)
        
        # Normalize weights
        total_weight = sum(weights)
        if total_weight == 0:
            return 0.0, 0.0
        
        normalized_weights = [w / total_weight for w in weights]
        
        # Calculate weighted average
        weighted_avg = sum(v * w for v, w in zip(values, normalized_weights))
        
        # Effective sample size (how many independent samples this represents)
        # Using Kish's formula: ESS = (sum(weights))^2 / sum(weights^2)
        ess = (sum(weights) ** 2) / sum(w ** 2 for w in weights) if sum(w ** 2 for w in weights) > 0 else len(values)
        
        return weighted_avg, ess
    
    @staticmethod
    def bayesian_win_rate(
        wins: int,
        losses: int,
        prior_wins: float = 1.0,
        prior_losses: float = 1.0,
        prior_strength: float = 2.0
    ) -> Tuple[float, float, float]:
        """
        Calculate Bayesian win rate with shrinkage toward prior
        
        Uses Beta-Binomial conjugate prior to handle small sample sizes
        
        Args:
            wins: Number of wins observed
            losses: Number of losses observed
            prior_wins: Prior belief for wins (default: 1 = uniform prior)
            prior_losses: Prior belief for losses (default: 1 = uniform prior)
            prior_strength: How strong the prior is (higher = more shrinkage)
        
        Returns:
            Tuple of (posterior_mean, posterior_lower_bound, posterior_upper_bound)
            (95% credible interval)
        """
        # Posterior parameters (Beta distribution)
        alpha = prior_wins * prior_strength + wins
        beta = prior_losses * prior_strength + losses
        
        # Posterior mean (expected win rate)
        posterior_mean = alpha / (alpha + beta) if (alpha + beta) > 0 else 0.5
        
        # 95% credible interval
        if alpha > 0 and beta > 0:
            lower = stats.beta.ppf(0.025, alpha, beta)
            upper = stats.beta.ppf(0.975, alpha, beta)
        else:
            lower = 0.0
            upper = 1.0
        
        return posterior_mean, lower, upper
    
    @staticmethod
    def weighted_win_rate(
        wins: List[float],
        losses: List[float],
        weights: Optional[List[float]] = None
    ) -> float:
        """
        Calculate weighted win rate
        
        Args:
            wins: List of win counts (can be fractional for weighted)
            losses: List of loss counts
            weights: Optional weights for each observation
        
        Returns:
            Weighted win rate
        """
        if not wins or len(wins) != len(losses):
            return 0.5
        
        if weights is None:
            weights = [1.0] * len(wins)
        
        total_weighted_wins = sum(w * weight for w, weight in zip(wins, weights))
        total_weighted_games = sum((w + l) * weight for w, l, weight in zip(wins, losses, weights))
        
        if total_weighted_games == 0:
            return 0.5
        
        return total_weighted_wins / total_weighted_games
    
    @staticmethod
    def robust_average(
        values: List[float],
        method: str = "trimmed",
        trim_percent: float = 0.1
    ) -> Tuple[float, float]:
        """
        Calculate robust average that handles outliers
        
        Args:
            values: List of values
            method: "trimmed" (remove outliers), "median" (use median), "winsorized" (cap outliers)
            trim_percent: Percentage to trim from each end (for trimmed mean)
        
        Returns:
            Tuple of (robust_average, standard_deviation)
        """
        if not values:
            return 0.0, 0.0
        
        values_array = np.array(values)
        
        if method == "median":
            robust_avg = np.median(values_array)
            std_dev = np.std(values_array)
        elif method == "trimmed":
            n_trim = int(len(values) * trim_percent)
            if n_trim > 0:
                sorted_values = np.sort(values_array)
                trimmed = sorted_values[n_trim:-n_trim] if n_trim > 0 else sorted_values
                robust_avg = np.mean(trimmed)
                std_dev = np.std(trimmed)
            else:
                robust_avg = np.mean(values_array)
                std_dev = np.std(values_array)
        elif method == "winsorized":
            n_winsorize = int(len(values) * trim_percent)
            if n_winsorize > 0:
                sorted_values = np.sort(values_array)
                lower_bound = sorted_values[n_winsorize]
                upper_bound = sorted_values[-n_winsorize]
                winsorized = np.clip(values_array, lower_bound, upper_bound)
                robust_avg = np.mean(winsorized)
                std_dev = np.std(winsorized)
            else:
                robust_avg = np.mean(values_array)
                std_dev = np.std(values_array)
        else:
            robust_avg = np.mean(values_array)
            std_dev = np.std(values_array)
        
        return float(robust_avg), float(std_dev)
    
    @staticmethod
    def normalize_probabilities(
        probs: Dict[str, float],
        method: str = "softmax"
    ) -> Dict[str, float]:
        """
        Normalize probabilities to sum to 1.0 using proper methods
        
        Args:
            probs: Dictionary of probabilities (can be unnormalized)
            method: "softmax" (log-space normalization), "linear" (simple division)
        
        Returns:
            Normalized probabilities
        """
        if not probs:
            return {}
        
        if method == "softmax":
            # Use log-space to avoid numerical issues
            max_log_prob = max(math.log(max(p, 1e-10)) for p in probs.values())
            exp_probs = {
                k: math.exp(math.log(max(p, 1e-10)) - max_log_prob)
                for k, p in probs.items()
            }
            total = sum(exp_probs.values())
            return {k: v / total for k, v in exp_probs.items()}
        else:  # linear
            total = sum(probs.values())
            if total == 0:
                # Equal probabilities if all zero
                n = len(probs)
                return {k: 1.0 / n for k in probs.keys()}
            return {k: v / total for k, v in probs.items()}
    
    @staticmethod
    def log_odds_to_probability(log_odds: float) -> float:
        """
        Convert log-odds to probability
        
        Args:
            log_odds: Log-odds value
        
        Returns:
            Probability (0 to 1)
        """
        return 1.0 / (1.0 + math.exp(-log_odds))
    
    @staticmethod
    def probability_to_log_odds(prob: float) -> float:
        """
        Convert probability to log-odds
        
        Args:
            prob: Probability (0 to 1)
        
        Returns:
            Log-odds value
        """
        if prob <= 0:
            return -float('inf')
        if prob >= 1:
            return float('inf')
        return math.log(prob / (1.0 - prob))
    
    @staticmethod
    def combine_probabilities(
        probs: List[float],
        weights: Optional[List[float]] = None,
        method: str = "log_odds"
    ) -> float:
        """
        Combine multiple probability estimates
        
        Args:
            probs: List of probabilities to combine
            weights: Optional weights for each probability
            method: "log_odds" (combine in log-odds space), "geometric" (geometric mean)
        
        Returns:
            Combined probability
        """
        if not probs:
            return 0.5
        
        if weights is None:
            weights = [1.0] * len(probs)
        
        if method == "log_odds":
            # Combine in log-odds space (more statistically sound)
            total_weight = sum(weights)
            if total_weight == 0:
                return 0.5
            
            weighted_log_odds = sum(
                StatisticalUtils.probability_to_log_odds(p) * w
                for p, w in zip(probs, weights)
            ) / total_weight
            
            return StatisticalUtils.log_odds_to_probability(weighted_log_odds)
        else:  # geometric mean
            # Geometric mean of probabilities
            weighted_log_probs = sum(
                math.log(max(p, 1e-10)) * w
                for p, w in zip(probs, weights)
            )
            total_weight = sum(weights)
            if total_weight == 0:
                return 0.5
            return math.exp(weighted_log_probs / total_weight)
    
    @staticmethod
    def confidence_interval(
        values: List[float],
        confidence: float = 0.95,
        method: str = "bootstrap"
    ) -> Tuple[float, float, float]:
        """
        Calculate confidence interval for a statistic
        
        Args:
            values: List of values
            confidence: Confidence level (0.95 for 95%)
            method: "bootstrap", "normal" (assumes normal distribution), "t" (t-distribution)
        
        Returns:
            Tuple of (mean, lower_bound, upper_bound)
        """
        if not values:
            return 0.0, 0.0, 0.0
        
        mean = np.mean(values)
        n = len(values)
        
        if method == "normal" or n >= 30:
            # Use normal approximation
            std_err = np.std(values, ddof=1) / math.sqrt(n)
            z_score = stats.norm.ppf((1 + confidence) / 2)
            margin = z_score * std_err
            return float(mean), float(mean - margin), float(mean + margin)
        elif method == "t":
            # Use t-distribution (better for small samples)
            std_err = np.std(values, ddof=1) / math.sqrt(n)
            t_score = stats.t.ppf((1 + confidence) / 2, df=n-1)
            margin = t_score * std_err
            return float(mean), float(mean - margin), float(mean + margin)
        else:  # bootstrap
            # Bootstrap confidence interval
            n_bootstrap = 1000
            bootstrap_means = []
            for _ in range(n_bootstrap):
                sample = np.random.choice(values, size=n, replace=True)
                bootstrap_means.append(np.mean(sample))
            
            alpha = 1 - confidence
            lower = np.percentile(bootstrap_means, 100 * alpha / 2)
            upper = np.percentile(bootstrap_means, 100 * (1 - alpha / 2))
            return float(mean), float(lower), float(upper)
    
    @staticmethod
    def regression_to_mean(
        observed: float,
        sample_size: int,
        population_mean: float,
        population_variance: float,
        sample_variance: Optional[float] = None
    ) -> float:
        """
        Apply regression to the mean (shrinkage estimator)
        
        Useful when sample size is small - shrink toward population mean
        
        Args:
            observed: Observed sample mean
            sample_size: Number of observations
            population_mean: Population/prior mean
            population_variance: Population variance
            sample_variance: Sample variance (if None, uses population_variance)
        
        Returns:
            Shrunk estimate
        """
        if sample_size == 0:
            return population_mean
        
        if sample_variance is None:
            sample_variance = population_variance
        
        # Calculate shrinkage factor (how much to shrink toward prior)
        # More shrinkage when sample is small or sample variance is high
        shrinkage_factor = population_variance / (
            population_variance + sample_variance / sample_size
        )
        
        # Shrink toward population mean
        shrunk_estimate = (
            shrinkage_factor * population_mean +
            (1 - shrinkage_factor) * observed
        )
        
        return shrunk_estimate
    
    @staticmethod
    def effective_sample_size(
        weights: List[float]
    ) -> float:
        """
        Calculate effective sample size from weights
        
        Uses Kish's formula: ESS = (sum(weights))^2 / sum(weights^2)
        
        Args:
            weights: List of weights
        
        Returns:
            Effective sample size
        """
        if not weights:
            return 0.0
        
        sum_weights = sum(weights)
        sum_squared_weights = sum(w ** 2 for w in weights)
        
        if sum_squared_weights == 0:
            return 0.0
        
        return (sum_weights ** 2) / sum_squared_weights

