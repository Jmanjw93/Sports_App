# Create Your .env File

Since the `.env` file is protected, please create it manually:

## Steps:

1. In the `sports-analytics-app` folder, create a new file named `.env`

2. Copy and paste this content into the file:

```env
# Weather API (OpenWeatherMap) - ✅ Your key is valid!
WEATHER_API_KEY=8277b9d832acb7bc96cabc045f69cac3

# Sports Data API (Optional - App works with mock data)
SPORTS_API_KEY=

# Database (Default SQLite - no setup needed)
DATABASE_URL=sqlite:///sports_analytics.db

# Server Configuration
API_HOST=0.0.0.0
API_PORT=8000

# CORS Settings
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

3. Save the file

That's it! Your weather API key is now configured and ready to use.

## Verification

Your API key has been tested and is **valid** ✅

The application will now use real weather data from OpenWeatherMap when making predictions!




