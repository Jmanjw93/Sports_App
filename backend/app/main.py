"""
Main FastAPI application for Sports Analytics & Betting Predictions
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import re

app = FastAPI(
    title="Sports Analytics API",
    description="Professional sports betting analytics with weather integration",
    version="1.0.0"
)

# Allowed frontends - includes production and preview Vercel URLs
# Vercel preview deployments have dynamic URLs, so we use a custom middleware
allowed_origins = [
    "https://sports-app-taupe.vercel.app",  # Vercel production
    "https://sports-app-git-main-jmanjw93s-projects.vercel.app",  # Vercel production branch
    "https://sports-7t1fi3av-jmanjw93s-projects.vercel.app",  # Vercel preview
    "https://sports-2rrf7xil8-jmanjw93s-projects.vercel.app",  # Vercel preview
    "http://localhost:3000",  # local dev
    "http://localhost:3001",  # local dev
]

def is_allowed_origin(origin: str) -> bool:
    """Check if origin is allowed, including any Vercel preview deployment"""
    if not origin:
        return False
    # Allow localhost for development
    if origin.startswith("http://localhost"):
        return True
    # Allow any Vercel deployment (production or preview) - matches *.vercel.app
    if re.match(r"^https://.*\.vercel\.app$", origin):
        return True
    # Check explicit allowed origins
    return origin in allowed_origins

# Custom CORS middleware that supports pattern matching for Vercel preview URLs
class FlexibleCORSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        origin = request.headers.get("origin")
        
        # Handle preflight OPTIONS requests
        if request.method == "OPTIONS":
            response = Response()
            if origin and is_allowed_origin(origin):
                response.headers["Access-Control-Allow-Origin"] = origin
                response.headers["Access-Control-Allow-Credentials"] = "true"
                response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
                response.headers["Access-Control-Allow-Headers"] = "*"
                response.headers["Access-Control-Max-Age"] = "3600"
            return response
        
        # Handle actual requests
        response = await call_next(request)
        
        if origin and is_allowed_origin(origin):
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
        
        return response

# Add the custom CORS middleware
app.add_middleware(FlexibleCORSMiddleware)

# make sure this is ABOVE your router includes
from app.routers import games, predictions, odds, bets, player_props, simulations, parlays, learning

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
