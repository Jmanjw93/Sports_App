# Load Testing with Locust

This document describes how to run load tests for the Sports Analytics API using Locust.

## Prerequisites

1. Install Locust:
```bash
pip install locust
```

2. Ensure the API is running on `http://localhost:8000`

## Running Load Tests

### Basic Usage

Start Locust with the default configuration:
```bash
cd backend
locust -f locustfile.py
```

Then open your browser to `http://localhost:8089` to access the Locust web interface.

### Command Line Options

Run with specific user count and spawn rate:
```bash
locust -f locustfile.py --users 100 --spawn-rate 10 --host http://localhost:8000
```

Run headless (no web UI):
```bash
locust -f locustfile.py --headless --users 100 --spawn-rate 10 --host http://localhost:8000 --run-time 5m
```

### Load Scenarios

The `locustfile.py` includes different user classes for different scenarios:

- **SportsAnalyticsUser**: Normal load (1-3 second wait between requests)
- **LightLoadUser**: Light load (2-5 second wait)
- **HeavyLoadUser**: Heavy load (0.5-1.5 second wait)
- **SpikeLoadUser**: Spike load (0.1-0.5 second wait)

To use a specific scenario:
```bash
locust -f locustfile.py --users 50 --spawn-rate 5 --host http://localhost:8000 SportsAnalyticsUser
```

## Test Endpoints

The load tests cover the following endpoints:

1. **GET /health** - Health check
2. **GET /api/games/upcoming** - Get upcoming games
3. **GET /api/predictions/game/{game_id}** - Get game prediction (most common)
4. **GET /api/predictions/player/{player_name}** - Get player prop prediction
5. **GET /api/odds** - Get betting odds
6. **GET /api/bets/recommendations** - Get betting recommendations
7. **GET /metrics** - Prometheus metrics

## Monitoring

While running load tests, monitor:

1. **Prometheus metrics** at `http://localhost:8000/metrics`
2. **Grafana dashboard** at `http://localhost:3001` (if running)
3. **API logs** for errors and performance issues

## Performance Targets

Typical performance targets:

- **Response time (p95)**: < 500ms
- **Response time (p99)**: < 1s
- **Error rate**: < 1%
- **Throughput**: > 100 requests/second

## Tips

1. Start with a small number of users and gradually increase
2. Monitor Redis cache hit rates - should be > 80% after warmup
3. Check database connection pool if using database
4. Monitor memory and CPU usage during tests
5. Run tests for at least 5-10 minutes to see steady-state performance

