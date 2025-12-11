# Monitoring and Observability

This document describes the monitoring setup using Prometheus and Grafana.

## Architecture

- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and dashboards
- **Redis**: Caching layer (monitored via metrics)

## Setup

### Using Docker Compose

Start all monitoring services:
```bash
cd backend
docker-compose up -d redis prometheus grafana
```

Services will be available at:
- **Redis**: `localhost:6379`
- **Prometheus**: `http://localhost:9090`
- **Grafana**: `http://localhost:3001` (admin/admin)

### Manual Setup

#### Prometheus

1. Install Prometheus
2. Copy `monitoring/prometheus.yml` to your Prometheus config directory
3. Update the target URL if needed
4. Start Prometheus

#### Grafana

1. Install Grafana
2. Add Prometheus as a data source:
   - URL: `http://localhost:9090`
   - Access: Server (default)
3. Import the dashboard from `monitoring/grafana/dashboards/sports-analytics-dashboard.json`

## Metrics

### HTTP Metrics

- `http_requests_total`: Total HTTP requests by method, endpoint, and status
- `http_request_duration_seconds`: Request duration histogram

### Prediction Metrics

- `predictions_total`: Total predictions made by sport and model type
- `prediction_accuracy`: Prediction accuracy percentage
- `prediction_confidence_avg`: Average prediction confidence

### Cache Metrics

- `cache_hits_total`: Total cache hits
- `cache_misses_total`: Total cache misses
- `cache_operations_total`: Total cache operations by type and status

### API Metrics

- `api_errors_total`: Total API errors by type and endpoint

### Database Metrics

- `db_queries_total`: Total database queries by operation and table
- `db_query_duration_seconds`: Database query duration histogram

### System Metrics

- `active_connections`: Number of active connections
- `redis_connected`: Redis connection status (1 = connected, 0 = disconnected)

## Accessing Metrics

### Prometheus Endpoint

The API exposes metrics at:
```
GET /metrics
```

### Prometheus UI

Access Prometheus UI at `http://localhost:9090` to:
- Query metrics
- View targets
- Check alerting rules
- Explore metrics

### Grafana Dashboards

Access Grafana at `http://localhost:3001` to view:
- HTTP request rates and latencies
- Prediction metrics
- Cache performance
- Error rates
- System health

## Example Queries

### Request Rate
```
rate(http_requests_total[5m])
```

### 95th Percentile Latency
```
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

### Cache Hit Rate
```
rate(cache_hits_total[5m]) / (rate(cache_hits_total[5m]) + rate(cache_misses_total[5m]))
```

### Error Rate
```
rate(api_errors_total[5m])
```

## Alerts (Future)

You can configure alerts in Prometheus for:
- High error rates (> 5%)
- High latency (p95 > 1s)
- Low cache hit rate (< 50%)
- Redis disconnection
- High database query times

## Troubleshooting

### Prometheus not scraping

1. Check if the API is running
2. Verify the target URL in `prometheus.yml`
3. Check Prometheus logs: `docker logs sports-analytics-prometheus`

### Grafana not showing data

1. Verify Prometheus data source is configured correctly
2. Check if Prometheus has data: query `up` in Prometheus UI
3. Verify dashboard queries are correct

### Metrics not appearing

1. Check if the API `/metrics` endpoint returns data
2. Verify Prometheus can reach the API
3. Check Prometheus target status in UI

