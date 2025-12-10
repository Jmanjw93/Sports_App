# API Keys Guide

## Required vs Optional

**Good News**: The application works with **mock data** by default, so API keys are **optional** for development and testing!

However, to get **real data**, you'll need API keys for the services below.

## API Keys Needed

### 1. Weather API Key (Recommended)

**Purpose**: Get real-time weather data for game locations to improve predictions

**Service**: OpenWeatherMap (Recommended - Free tier available)

**How to Get It**:
1. Go to https://openweathermap.org/api
2. Sign up for a free account
3. Navigate to "API Keys" in your account dashboard
4. Copy your API key
5. Free tier includes: 60 calls/minute, 1,000,000 calls/month

**Add to `.env`**:
```env
WEATHER_API_KEY=your_openweathermap_api_key_here
```

**Alternative Services**:
- WeatherAPI.com (https://www.weatherapi.com/) - Free tier: 1M calls/month
- AccuWeather API (https://developer.accuweather.com/) - Free tier: 50 calls/day

---

### 2. Sports Data API Key (Recommended)

**Purpose**: Get real team statistics, player data, and game schedules

**Recommended Services**:

#### Option A: TheSportsDB (Free - Easiest to Start)
- **URL**: https://www.thesportsdb.com/api.php
- **Free Tier**: Unlimited requests (with rate limiting)
- **How to Get**: No API key needed! Just use the base URL
- **Note**: This is the easiest option to get started

#### Option B: API-Sports (Free Tier Available)
- **URL**: https://api-sports.io/
- **Free Tier**: 100 requests/day
- **How to Get**:
  1. Sign up at https://rapidapi.com/api-sports/api/api-sports
  2. Subscribe to the free plan
  3. Get your API key from the dashboard
- **Add to `.env`**:
  ```env
  SPORTS_API_KEY=your_api_sports_key_here
  ```

#### Option C: SportsDataIO (Paid - Most Comprehensive)
- **URL**: https://sportsdata.io/
- **Pricing**: Starts at $10/month
- **Best for**: Production use with high data quality

#### Option D: ESPN API
- Check ESPN's developer portal
- May require approval process

**Add to `.env`**:
```env
SPORTS_API_KEY=your_sports_api_key_here
```

---

### 3. Betting Odds API Keys (Advanced - Optional)

**Important**: Real betting odds APIs typically require:
- Legal/commercial agreements
- Business verification
- Paid subscriptions
- Compliance with sportsbook terms

#### bet365
- **Status**: Limited public API access
- **How to Get**: Contact bet365 business development
- **Note**: May require commercial partnership

#### DraftKings
- **URL**: https://sportsbook.draftkings.com/apis
- **Status**: Requires business agreement
- **How to Get**: Contact DraftKings API team
- **Note**: Primarily for commercial partners

#### TheScore Bet
- **Status**: Limited API access
- **How to Get**: Contact TheScore Bet business development
- **Note**: May require partnership agreement

**Current Status**: The application uses **mock odds data** for development. To integrate real odds, you'll need to:
1. Contact each sportsbook's business development team
2. Sign commercial agreements
3. Implement their specific API protocols
4. Handle authentication and rate limiting

**Alternative**: Some third-party services aggregate odds:
- OddsAPI (https://the-odds-api.com/) - Free tier: 500 requests/month
- BetAPI (https://betapi.io/) - Paid service

---

## Complete `.env` File Example

Create a `.env` file in the project root:

```env
# Weather API (Recommended - Free tier available)
WEATHER_API_KEY=your_openweathermap_key_here

# Sports Data API (Optional - App works with mock data)
SPORTS_API_KEY=your_sports_api_key_here

# Database (Default SQLite - no setup needed)
DATABASE_URL=sqlite:///sports_analytics.db

# Server Configuration (Optional - defaults work fine)
API_HOST=0.0.0.0
API_PORT=8000

# CORS (Optional - defaults work for local development)
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

## Quick Start Without API Keys

You can run the application **immediately** without any API keys! The app will use mock data:

1. **No `.env` file needed** - The app will work with defaults
2. **Mock sports data** - Sample games and teams
3. **Mock weather data** - Sample weather conditions
4. **Mock betting odds** - Sample odds from all platforms

This is perfect for:
- Testing the application
- Understanding how it works
- Developing new features
- Learning the betting methods

## Recommended Setup for Production

For a production-ready setup, get at minimum:

1. **OpenWeatherMap API Key** (Free)
   - Easy to get
   - Improves prediction accuracy
   - Free tier is generous

2. **TheSportsDB** (Free - No key needed)
   - Easiest sports data option
   - No signup required
   - Good for getting started

3. **API-Sports** (Free tier)
   - Better data quality
   - More comprehensive stats
   - 100 requests/day free tier

## Testing Your API Keys

Once you add API keys, you can test them:

### Test Weather API
```bash
curl "http://api.openweathermap.org/data/2.5/weather?q=New%20York&appid=YOUR_KEY&units=imperial"
```

### Test Sports API
Depends on which service you're using. Check their documentation.

## Troubleshooting

### "API key not working"
- Verify the key is correct (no extra spaces)
- Check if the service requires account activation
- Verify rate limits haven't been exceeded
- Check service status page

### "Getting 401/403 errors"
- API key might be invalid
- Account might need activation
- Free tier limits might be exceeded

### "No data showing"
- The app falls back to mock data automatically
- Check console logs for API errors
- Verify `.env` file is in the correct location (project root)

## Summary

**Minimum to Run**: **0 API keys** (uses mock data)

**Recommended**: 
- 1 API key: OpenWeatherMap (free, improves accuracy)

**For Production**:
- 2 API keys: OpenWeatherMap + Sports Data API (TheSportsDB or API-Sports)

**Betting Odds**: Currently mock data. Real integration requires commercial agreements.


