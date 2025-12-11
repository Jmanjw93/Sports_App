"""
Main FastAPI application for Sports Analytics & Betting Predictions
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import games, predictions, odds, bets
from app.config import settings

app = FastAPI(
    title="Sports Analytics API",
    description="Professional sports betting analytics with weather integration",
    version="1.0.0"
)

# Try to initialize database (optional)
try:
    from app.database import init_db
    init_db()
except Exception as e:
    print(f"Database initialization skipped: {e}")

# Try to initialize Redis cache (optional)
try:
    from app.cache.redis_cache import get_cache
    cache = get_cache()
    if cache.enabled:
        try:
            from app.monitoring.prometheus_metrics import set_redis_status
            set_redis_status(True)
        except:
            pass
except Exception as e:
    print(f"Redis cache initialization skipped: {e}")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Metrics middleware (optional, must be after CORS)
try:
    from app.monitoring.middleware import MetricsMiddleware
    app.add_middleware(MetricsMiddleware)
except Exception as e:
    print(f"Metrics middleware skipped: {e}")

# Include routers
app.include_router(games.router, prefix="/api/games", tags=["games"])
app.include_router(predictions.router, prefix="/api/predictions", tags=["predictions"])
app.include_router(odds.router, prefix="/api/odds", tags=["odds"])
app.include_router(bets.router, prefix="/api/bets", tags=["bets"])

# ML predictions router (optional)
try:
    from app.routers import ml_predictions
    app.include_router(ml_predictions.router, prefix="/api/ml-predictions", tags=["ml-predictions"])
except Exception as e:
    print(f"ML predictions router skipped: {e}")

# Prometheus metrics endpoint (optional)
try:
    from app.monitoring.prometheus_metrics import metrics_response
    @app.get("/metrics")
    async def metrics():
        """Prometheus metrics endpoint"""
        return metrics_response()
except Exception as e:
    print(f"Metrics endpoint skipped: {e}")


@app.get("/")
async def root():
    return {
        "message": "Sports Analytics API",
        "version": "1.0.0",
        "endpoints": {
            "games": "/api/games",
            "predictions": "/api/predictions",
            "odds": "/api/odds",
            "bets": "/api/bets"
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

