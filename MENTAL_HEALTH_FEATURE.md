# Mental Health & Psychology Analysis Feature

## Overview
The mental health analysis feature integrates psychological factors and player mental health into game prediction calculations. This provides a more comprehensive view of team performance by considering factors beyond just physical statistics.

## How It Works

### Player-Level Analysis
The system analyzes individual players' mental health based on:

1. **Recent Performance Trends**
   - Comparing recent games (last 3) to season average
   - Identifying improving, declining, or stable trends
   - Impact on confidence and stress levels

2. **Contract Status**
   - Contract negotiations (increased stress, reduced focus)
   - Contract year (increased motivation)
   - Recently signed contracts (boosted confidence)

3. **Personal Life Events**
   - Family issues (reduced focus, increased stress)
   - Positive life events (increased motivation)
   - Media scrutiny (increased stress, reduced focus)

4. **Experience Factors**
   - Veteran players (better pressure handling)
   - Young players (less experience with pressure)
   - Position-specific pressures (QB, PG, P positions have higher stress)

### Team-Level Analysis
The system analyzes team-wide mental health factors:

1. **Team Chemistry**
   - How well players work together
   - Affected by coaching stability, recent performance

2. **Team Morale**
   - Win/loss streaks impact morale significantly
   - 3+ game winning streak: +15% morale boost
   - 3+ game losing streak: -20% morale reduction

3. **Pressure Handling**
   - Playoff game pressure
   - High-stakes situations
   - Media pressure

4. **Key Player Mental Health**
   - Average mental health of key players
   - Weighted impact on team performance

## Impact on Predictions

### Calculation
- **Team Mental Health Score**: Weighted combination of chemistry (30%), morale (30%), pressure handling (20%), and key player impact (20%)
- **Individual Player Impact**: Based on confidence, stress, focus, and motivation levels
- **Net Adjustment**: Difference between home and away team mental health impacts
- **Win Probability Adjustment**: Applied to base probabilities (weight: 12% for team factors, 15% for key players)

### Example Impact
- Strong mental health (70%+ score) with good chemistry and morale: +2-4% win probability boost
- Poor mental health (below 50%) with low morale: -2-4% win probability reduction
- Key player with declining trend and high stress: -1-2% individual impact

## Factors Considered

### Player Factors
- Recent performance vs. season average
- Contract negotiations/status
- Personal life events
- Media attention
- Age and experience
- Position pressure

### Team Factors
- Win/loss streaks
- Playoff pressure
- Coaching stability
- Media scrutiny
- Team chemistry
- Key player mental states

## API Response

The mental health impact is included in the game prediction response:

```json
{
  "mental_health_impact": {
    "home_team": {
      "overall_score": 0.75,
      "team_chemistry": 0.80,
      "morale": 0.70,
      "pressure_handling": 0.65,
      "impact_on_win_probability": 0.02,
      "factors": ["3-game winning streak", "Strong team chemistry"],
      "key_players": [
        {
          "player_name": "Player 1",
          "position": "QB",
          "overall_score": 0.78,
          "confidence_level": 0.85,
          "stress_level": 0.25,
          "focus_level": 0.80,
          "motivation_level": 0.75,
          "recent_trend": "improving",
          "factors": ["Strong recent performance boost"],
          "impact_on_performance": 0.08
        }
      ]
    },
    "away_team": {
      // Similar structure
    },
    "net_adjustment": 0.015,
    "summary": "Home team has strong mental health (75% score) with better team chemistry and morale, giving them a 1.5% advantage"
  }
}
```

## Frontend Display

The mental health impact is displayed in the game card with:
- Overall summary of mental health impact
- Team scores (chemistry, morale, pressure handling)
- Key factors affecting each team
- Expandable key player mental health details
- Net win probability adjustment

## Future Enhancements

Potential improvements:
1. **Real Data Integration**
   - Connect to player performance databases
   - Integrate with news/social media sentiment analysis
   - Track contract negotiations from public sources

2. **Advanced Metrics**
   - Sleep quality and recovery data
   - Travel fatigue impact
   - Home/away mental health differences
   - Historical mental health patterns

3. **Machine Learning**
   - Train models on historical mental health vs. performance data
   - Predict mental health trends
   - Identify at-risk players/teams

4. **Real-Time Updates**
   - Live updates during game week
   - Breaking news impact analysis
   - Injury recovery mental health tracking

## Technical Details

### Files Modified
- `backend/app/models/mental_health_analyzer.py` - New module for mental health analysis
- `backend/app/models/prediction_models.py` - Integrated mental health into predictions
- `backend/app/routers/predictions.py` - Added mental health to API response
- `frontend/components/GameCard.tsx` - Added mental health display

### Weights and Tuning
- Mental health weight: 12% of team factors
- Key player weight: 15% of individual impacts
- These can be adjusted based on validation against historical results

## Notes

- Currently uses mock data for demonstration
- In production, would integrate with real player/team databases
- Mental health scores are normalized (0.0 to 1.0)
- Impact adjustments are conservative to avoid over-weighting psychological factors




