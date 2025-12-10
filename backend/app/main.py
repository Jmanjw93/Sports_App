"""
Main FastAPI application for Sports Analytics & Betting Predictions
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import games, predictions, odds, bets, player_props, simulations, parlays, learning
from app.config import settings

app = FastAPI(
    title="Sports Analytics API",
    description="Professional sports betting analytics with weather integration",
    version="1.0.0"
)

# CORS middleware
# Note: If allow_origins contains ["*"], allow_credentials must be False
cors_origins = settings.cors_origins_list
allow_creds = "*" not in cors_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=allow_creds,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(games.router, prefix="/api/games", tags=["games"])
app.include_router(predictions.router, prefix="/api/predictions", tags=["predictions"])
app.include_router(odds.router, prefix="/api/odds", tags=["odds"])
app.include_router(bets.router, prefix="/api/bets", tags=["bets"])
app.include_router(player_props.router, prefix="/api/player-props", tags=["player-props"])
app.include_router(simulations.router, prefix="/api/simulations", tags=["simulations"])
app.include_router(parlays.router, prefix="/api/parlays", tags=["parlays"])
app.include_router(learning.router, prefix="/api/learning", tags=["learning"])


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

