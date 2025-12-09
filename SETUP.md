# Setup Instructions

## Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- npm or yarn

## Backend Setup

1. Navigate to the project directory:
```bash
cd sports-analytics-app
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file in the project root (copy from `.env.example`):
```bash
# Copy the example file and fill in your API keys
SPORTS_API_KEY=your_sports_api_key_here
WEATHER_API_KEY=your_weather_api_key_here
DATABASE_URL=sqlite:///sports_analytics.db
```

6. Run the backend server:
```bash
cd backend
python -m uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env.local` file:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Getting API Keys

### Sports Data API
You can use one of these services:
- **TheSportsDB**: https://www.thesportsdb.com/api.php (Free tier available)
- **API-Sports**: https://api-sports.io/ (Free tier available)
- **SportsDataIO**: https://sportsdata.io/ (Paid)
- **ESPN API**: Check ESPN's developer portal

### Weather API
- **OpenWeatherMap**: https://openweathermap.org/api (Free tier available)
  - Sign up and get your API key
  - Add it to your `.env` file as `WEATHER_API_KEY`

## Betting Odds APIs

**Important**: Real-time betting odds APIs typically require:
- Legal agreements with the sportsbook
- Commercial licenses
- Rate limiting compliance

For development, the application uses mock data. To integrate real odds:

1. **bet365**: Check their developer program (if available)
2. **DraftKings**: https://sportsbook.draftkings.com/apis (Requires agreement)
3. **TheScore Bet**: Contact their business development team

**Note**: Web scraping betting sites may violate their Terms of Service. Always check and comply with their policies.

## Running the Application

### Option 1: Run separately

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Option 2: Use batch scripts (Windows)

**Backend:**
```bash
start_backend.bat
```

**Frontend:**
```bash
start_frontend.bat
```

## Testing the API

Once the backend is running, you can test it:

```bash
# Get upcoming games
curl http://localhost:8000/api/games/?sport=nfl

# Get game prediction
curl http://localhost:8000/api/predictions/game/{game_id}

# Get best bets
curl http://localhost:8000/api/bets/best-bets?sport=nfl
```

## Troubleshooting

### Backend Issues
- Make sure Python 3.9+ is installed
- Check that all dependencies are installed: `pip list`
- Verify your `.env` file exists and has correct values
- Check the console for error messages

### Frontend Issues
- Make sure Node.js 18+ is installed
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Check that the backend is running on port 8000
- Verify `.env.local` has the correct API URL

### CORS Issues
- Make sure CORS_ORIGINS in `.env` includes `http://localhost:3000`
- Check that both servers are running

## Next Steps

1. Replace mock data with real API integrations
2. Add database for storing historical predictions
3. Implement machine learning models for better predictions
4. Add user authentication and saved bets
5. Implement real-time odds updates
6. Add more sports and betting markets

