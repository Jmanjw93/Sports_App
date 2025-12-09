# Sports Analytics & Betting Prediction Application

A comprehensive sports analytics application that uses professional betting methods to predict game outcomes and identify the best player bets with optimal odds from bet365, DraftKings, and TheScore Bet.

## Features

- **Weather Integration**: Factors in weather conditions for outdoor sports
- **Professional Betting Methods**: Uses Expected Value (EV), Kelly Criterion, and advanced statistical models
- **Multi-Platform Odds Comparison**: Aggregates and compares odds from bet365, DraftKings, and TheScore Bet
- **Team Win Predictions**: Advanced models to predict game winners
- **Player Prop Bets**: Identifies the best player-specific betting opportunities
- **Real-time Data**: Fetches live sports data, weather, and betting odds

## Project Structure

```
sports-analytics-app/
├── backend/              # Python backend API
│   ├── app/             # Main application
│   ├── models/          # ML and statistical models
│   ├── data/            # Data collection modules
│   └── utils/           # Utility functions
├── frontend/            # React/Next.js frontend
└── requirements.txt     # Python dependencies
```

## Setup

### Backend Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables (create `.env` file):
```
SPORTS_API_KEY=your_api_key
WEATHER_API_KEY=your_weather_api_key
DATABASE_URL=sqlite:///sports_analytics.db
```

3. Run the backend server:
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Run the development server:
```bash
npm run dev
```

## API Endpoints

- `GET /api/games` - Get upcoming games
- `GET /api/predictions/{game_id}` - Get predictions for a game
- `GET /api/best-bets` - Get best betting opportunities
- `GET /api/odds/{game_id}` - Get odds from all platforms

## Betting Methods Used

1. **Expected Value (EV)**: Calculates the expected return on each bet
2. **Kelly Criterion**: Determines optimal bet sizing
3. **Weather Impact Analysis**: Adjusts predictions based on weather conditions
4. **Historical Performance**: Uses team and player historical data
5. **Injury Reports**: Factors in player availability

## Disclaimer

This application is for educational and analytical purposes only. Always gamble responsibly and within your means.

