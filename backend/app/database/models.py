"""
Database models for sports analytics using SQLAlchemy
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Team(Base):
    """Team model"""
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    sport = Column(String(10), index=True, nullable=False)  # nfl, nba, mlb, nhl
    city = Column(String(50))
    state = Column(String(2))
    abbreviation = Column(String(10))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    games_home = relationship("Game", foreign_keys="Game.home_team_id", back_populates="home_team")
    games_away = relationship("Game", foreign_keys="Game.away_team_id", back_populates="away_team")
    stats = relationship("TeamStats", back_populates="team")
    players = relationship("Player", back_populates="team")


class Player(Base):
    """Player model"""
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"))
    position = Column(String(10))
    sport = Column(String(10), index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    team = relationship("Team", back_populates="players")
    stats = relationship("PlayerStats", back_populates="player")
    props = relationship("PlayerProp", back_populates="player")


class Game(Base):
    """Game model"""
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(String(100), unique=True, index=True, nullable=False)
    sport = Column(String(10), index=True, nullable=False)
    home_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    away_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    game_date = Column(DateTime, index=True, nullable=False)
    venue = Column(String(200))
    location_city = Column(String(50))
    location_state = Column(String(2))
    location_country = Column(String(50))
    location_lat = Column(Float)
    location_lon = Column(Float)
    status = Column(String(20), default="scheduled")  # scheduled, in_progress, completed, cancelled
    home_score = Column(Integer)
    away_score = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    home_team = relationship("Team", foreign_keys=[home_team_id], back_populates="games_home")
    away_team = relationship("Team", foreign_keys=[away_team_id], back_populates="games_away")
    predictions = relationship("Prediction", back_populates="game")
    weather = relationship("GameWeather", back_populates="game", uselist=False)


class TeamStats(Base):
    """Team statistics model"""
    __tablename__ = "team_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    season = Column(String(10), index=True)  # e.g., "2024-2025"
    win_rate = Column(Float)
    points_per_game = Column(Float)
    points_allowed_per_game = Column(Float)
    recent_form = Column(Float)  # Last 5-10 games performance
    home_wins = Column(Integer, default=0)
    home_losses = Column(Integer, default=0)
    away_wins = Column(Integer, default=0)
    away_losses = Column(Integer, default=0)
    strength_of_schedule = Column(Float)
    stats_json = Column(JSON)  # Additional stats as JSON
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    team = relationship("Team", back_populates="stats")


class PlayerStats(Base):
    """Player statistics model"""
    __tablename__ = "player_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    season = Column(String(10), index=True)
    position = Column(String(10))
    consistency = Column(Float)
    recent_trend = Column(Float)
    stats_json = Column(JSON)  # Position-specific stats
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    player = relationship("Player", back_populates="stats")


class Prediction(Base):
    """Prediction model"""
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    predicted_winner = Column(String(100))
    home_win_probability = Column(Float, nullable=False)
    away_win_probability = Column(Float, nullable=False)
    confidence = Column(Float)
    model_type = Column(String(50))  # basic, ml, ensemble
    prediction_data = Column(JSON)  # Full prediction details
    actual_winner = Column(String(100))  # Set after game completion
    is_correct = Column(Boolean)  # True if prediction was correct
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    game = relationship("Game", back_populates="predictions")


class PlayerProp(Base):
    """Player prop prediction model"""
    __tablename__ = "player_props"
    
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"))
    prop_type = Column(String(50), nullable=False)  # points, yards, touchdowns, etc.
    predicted_value = Column(Float, nullable=False)
    line = Column(Float)  # Betting line
    over_probability = Column(Float)
    under_probability = Column(Float)
    confidence = Column(Float)
    actual_value = Column(Float)  # Set after game
    is_over = Column(Boolean)  # True if actual > line
    is_correct = Column(Boolean)  # True if prediction was correct
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    player = relationship("Player", back_populates="props")


class GameWeather(Base):
    """Game weather data model"""
    __tablename__ = "game_weather"
    
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), unique=True, nullable=False)
    temperature = Column(Float)
    wind_speed = Column(Float)
    precipitation = Column(Float)
    conditions = Column(String(50))  # clear, rain, snow, etc.
    humidity = Column(Float)
    weather_data = Column(JSON)  # Full weather data
    forecast_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    game = relationship("Game", back_populates="weather")


class Injury(Base):
    """Injury data model"""
    __tablename__ = "injuries"
    
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    injury_type = Column(String(100))
    status = Column(String(50))  # out, questionable, probable, etc.
    injury_date = Column(DateTime)
    expected_return = Column(DateTime)
    is_key_player = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

