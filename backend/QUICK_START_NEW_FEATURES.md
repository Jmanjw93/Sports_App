# Quick Start Guide - New Features

This guide helps you quickly set up and use the new features.

## Prerequisites

1. Python 3.8+
2. Docker and Docker Compose (for Redis, Prometheus, Grafana)
3. pip

## Installation

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Start Supporting Services

Start Redis, Prometheus, and Grafana:
```bash
docker-compose up -d
```

This starts:
- Redis on port 6379
- Prometheus on port 9090
- Grafana on port 3001

### 3. Start the API

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Using the Features

### 1. ML Predictions

Get ML-based predictions:
```bash
# Ensemble model (recommended)
curl http://localhost:8000/api/ml-predictions/game/nfl_1_1734567890?model_type=ensemble

# Specific model
curl http://localhost:8000/api/ml-predictions/game/nfl_1_1734567890?model_type=xgboost

# Player prop prediction
curl "http://localhost:8000/api/ml-predictions/player/Patrick%20Mahomes?prop_type=points"
```

### 2. Caching

Caching is automatic! The first request will be slower, subsequent requests will be faster.

Check cache status:
```bash
# Redis should be running
docker ps | grep redis
```

### 3. Monitoring

View metrics:
```bash
# Prometheus metrics endpoint
curl http://localhost:8000/metrics

# Prometheus UI
open http://localhost:9090

# Grafana UI
open http://localhost:3001
# Login: admin/admin
```

### 4. Load Testing

Run load tests:
```bash
# Start Locust
locust -f locustfile.py

# Open browser to http://localhost:8089
# Or run headless:
locust -f locustfile.py --headless --users 50 --spawn-rate 5 --run-time 5m
```

## Configuration

### Environment Variables

Create a `.env` file:
```env
# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Database
DATABASE_URL=sqlite:///./sports_analytics.db

# API Keys (if needed)
SPORTS_API_KEY=your_key_here
WEATHER_API_KEY=your_key_here
```

## Verification

### Check Redis Connection
```python
from app.cache.redis_cache import get_cache
cache = get_cache()
print(f"Redis enabled: {cache.enabled}")
```

### Check Metrics
```bash
curl http://localhost:8000/metrics | grep http_requests_total
```

### Check Database
```python
from app.database import init_db
init_db()  # Creates tables if they don't exist
```

## Troubleshooting

### Redis Connection Failed
- Check if Redis is running: `docker ps | grep redis`
- Check Redis logs: `docker logs sports-analytics-redis`
- The API will work without Redis, but caching will be disabled

### Prometheus Not Scraping
- Check if API is running on port 8000
- Verify target in Prometheus UI: http://localhost:9090/targets
- Check `monitoring/prometheus.yml` configuration

### ML Models Not Working
- Ensure scikit-learn and xgboost are installed
- Check logs for model loading errors
- Models will train automatically on first use (using synthetic data)

## Next Steps

1. **Train Real Models**: Replace synthetic training data with historical game data
2. **Configure Alerts**: Set up Prometheus alerts for production
3. **Tune Cache TTLs**: Adjust cache expiration based on your needs
4. **Run Load Tests**: Validate performance under load
5. **Monitor Performance**: Use Grafana dashboards to track metrics

## Documentation

- `FEATURES_SUMMARY.md`: Detailed feature documentation
- `LOAD_TESTING.md`: Load testing guide
- `MONITORING.md`: Monitoring setup guide

