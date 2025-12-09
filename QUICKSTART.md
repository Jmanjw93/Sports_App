# Quick Start Guide

Get up and running with the Sports Analytics application in 5 minutes!

## Step 1: Install Dependencies

### Backend
```bash
cd sports-analytics-app
pip install -r requirements.txt
```

### Frontend
```bash
cd frontend
npm install
```

## Step 2: Configure Environment

Create a `.env` file in the project root:
```env
SPORTS_API_KEY=your_key_here
WEATHER_API_KEY=your_key_here
DATABASE_URL=sqlite:///sports_analytics.db
```

**Note**: The app works with mock data if you don't have API keys yet!

## Step 3: Start the Application

### Terminal 1 - Backend
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```

## Step 4: Open Your Browser

Navigate to: **http://localhost:3000**

## What You'll See

1. **Games & Predictions Tab**: View upcoming games and get win probability predictions
2. **Best Team Bets Tab**: See betting opportunities with Expected Value calculations
3. **Player Props Tab**: (Coming soon) Player-specific betting recommendations

## Features Available

✅ Game outcome predictions with weather integration
✅ Expected Value (EV) calculations
✅ Kelly Criterion for optimal bet sizing
✅ Multi-platform odds comparison (bet365, DraftKings, TheScore Bet)
✅ Professional betting recommendations
✅ Modern, responsive UI

## API Endpoints

- `GET /api/games/` - List upcoming games
- `GET /api/predictions/game/{game_id}` - Get game prediction
- `GET /api/bets/best-bets` - Get best betting opportunities
- `GET /api/odds/game/{game_id}` - Get odds from all platforms

## Next Steps

1. Get API keys for real sports data (see SETUP.md)
2. Integrate real betting odds APIs
3. Customize the models for your betting strategy
4. Add more sports and betting markets

Enjoy analyzing and betting smarter! 🎯

