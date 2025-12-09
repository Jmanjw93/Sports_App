# Features & Betting Methods

## Core Features

### 1. Game Outcome Predictions
- **Statistical Analysis**: Uses team performance metrics (win rate, points per game, recent form)
- **Home Advantage**: Factors in home field advantage (typically 3% boost)
- **Weather Integration**: Adjusts predictions based on weather conditions
- **Confidence Scoring**: Provides confidence levels for each prediction

### 2. Weather Impact Analysis
- **Temperature Effects**: Extreme cold or heat affects player performance
- **Wind Impact**: High wind speeds (>20 mph) significantly impact passing games
- **Precipitation**: Rain/snow favors ground-based offenses
- **Visibility**: Poor visibility affects gameplay

### 3. Professional Betting Methods

#### Expected Value (EV) Calculation
Expected Value is the average amount you can expect to win or lose per bet over time.

**Formula**: `EV = (Win Probability × (Odds - 1)) - (Lose Probability × 1)`

- **Positive EV**: Bet is profitable in the long run
- **Negative EV**: Bet loses money over time
- **Zero EV**: Break-even scenario

**Example**:
- True win probability: 60% (0.60)
- Bookmaker odds: 2.00 (even money)
- EV = (0.60 × (2.00 - 1)) - (0.40 × 1) = 0.20 = +20%

This means you can expect a 20% return on average for this bet.

#### Kelly Criterion
Determines the optimal bet size to maximize long-term growth while avoiding bankruptcy.

**Formula**: `Kelly % = (bp - q) / b`
- `b` = odds - 1
- `p` = win probability
- `q` = 1 - p

**Fractional Kelly**: The app uses 25% of full Kelly (quarter Kelly) for safety:
- Reduces volatility
- Protects bankroll
- More conservative approach

**Example**:
- Win probability: 60%
- Odds: 2.00
- Full Kelly: (1 × 0.60 - 0.40) / 1 = 0.20 = 20%
- Quarter Kelly: 20% × 0.25 = 5%

So you should bet 5% of your bankroll on this opportunity.

#### Betting Recommendations
The app categorizes bets into:
- **Strong Bet**: EV > 10% and Kelly > 1%
- **Moderate Bet**: EV > 5% and Kelly > 0.5%
- **Small Bet**: EV > 0% but below moderate thresholds
- **Avoid**: Negative or zero EV

### 4. Multi-Platform Odds Comparison
- **bet365**: One of the world's largest sportsbooks
- **DraftKings**: Major US sportsbook
- **TheScore Bet**: Canadian/US sportsbook

The app compares odds across all platforms and identifies:
- Best odds for each bet
- Arbitrage opportunities
- Value bets

### 5. Player Prop Predictions
- **Historical Performance**: Uses player's average stats
- **Matchup Analysis**: Factors in opponent's defensive strength
- **Consistency Metrics**: Accounts for player reliability
- **Over/Under Probabilities**: Calculates likelihood of going over/under the line

## Data Sources

### Sports Data
- Team statistics (win rate, points per game, recent form)
- Player statistics (averages, trends, consistency)
- Game schedules and venues
- Historical matchups

### Weather Data
- Current conditions
- Forecast data
- Impact analysis on gameplay

### Betting Odds
- Real-time odds from multiple platforms
- Line movements
- Market analysis

## Model Architecture

### Game Prediction Model
1. **Base Strength Calculation**: Combines multiple team metrics
2. **Home Advantage Adjustment**: Adds home field boost
3. **Weather Adjustment**: Modifies probabilities based on conditions
4. **Confidence Calculation**: Based on probability difference

### Player Prop Model
1. **Base Prediction**: Historical average
2. **Matchup Factor**: Opponent defensive rating
3. **Probability Distribution**: Normal distribution approximation
4. **Over/Under Calculation**: Z-score based probabilities

### Betting Analysis Engine
1. **EV Calculation**: For each betting opportunity
2. **Kelly Sizing**: Optimal bet size recommendation
3. **Platform Comparison**: Finds best odds
4. **Risk Assessment**: Categorizes bet quality

## Key Metrics Explained

### True Probability
The model's calculated probability of an outcome occurring. This is compared against the bookmaker's implied probability to find value.

### Implied Probability
The probability implied by the bookmaker's odds: `1 / Decimal Odds`

### Expected Value (EV)
The expected return on investment. Positive EV means profitable long-term.

### Kelly Percentage
The recommended percentage of your bankroll to bet on this opportunity.

### Confidence
For game predictions, this is the difference between win probabilities. Higher confidence means a clearer favorite.

## Best Practices

1. **Bankroll Management**: Never bet more than the Kelly percentage recommends
2. **Diversification**: Spread bets across multiple games
3. **Value Betting**: Focus on positive EV bets, not just favorites
4. **Weather Awareness**: Pay attention to weather impacts, especially for outdoor sports
5. **Line Shopping**: Always compare odds across platforms
6. **Record Keeping**: Track your bets and results
7. **Discipline**: Stick to the recommendations, avoid emotional betting

## Limitations

- **Mock Data**: Currently uses mock data for development. Replace with real APIs for production.
- **Simplified Models**: Real-world betting requires more complex models
- **No Guarantees**: Past performance doesn't guarantee future results
- **Legal Compliance**: Ensure betting is legal in your jurisdiction
- **API Access**: Real odds APIs may require commercial agreements

## Future Enhancements

- Machine learning models for better predictions
- Real-time odds updates
- Historical performance tracking
- User accounts and saved bets
- More sports and betting markets
- Advanced analytics dashboard
- Bet tracking and ROI analysis

