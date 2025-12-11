"""
Prometheus metrics for monitoring
"""
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response
from typing import Optional
import time

# Request metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint'],
    buckets=[0.1, 0.5, 1.0, 2.5, 5.0, 10.0]
)

# Prediction metrics
predictions_total = Counter(
    'predictions_total',
    'Total predictions made',
    ['sport', 'model_type']
)

prediction_accuracy = Gauge(
    'prediction_accuracy',
    'Prediction accuracy percentage',
    ['sport', 'model_type']
)

prediction_confidence_avg = Gauge(
    'prediction_confidence_avg',
    'Average prediction confidence',
    ['sport']
)

# Cache metrics
cache_hits_total = Counter(
    'cache_hits_total',
    'Total cache hits',
    ['cache_type']
)

cache_misses_total = Counter(
    'cache_misses_total',
    'Total cache misses',
    ['cache_type']
)

cache_operations_total = Counter(
    'cache_operations_total',
    'Total cache operations',
    ['operation', 'status']
)

# API metrics
api_errors_total = Counter(
    'api_errors_total',
    'Total API errors',
    ['error_type', 'endpoint']
)

# Database metrics
db_queries_total = Counter(
    'db_queries_total',
    'Total database queries',
    ['operation', 'table']
)

db_query_duration_seconds = Histogram(
    'db_query_duration_seconds',
    'Database query duration in seconds',
    ['operation', 'table'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.0]
)

# System metrics
active_connections = Gauge(
    'active_connections',
    'Number of active connections'
)

redis_connected = Gauge(
    'redis_connected',
    'Redis connection status (1 = connected, 0 = disconnected)'
)


def record_request(method: str, endpoint: str, status_code: int, duration: float):
    """Record HTTP request metrics"""
    http_requests_total.labels(method=method, endpoint=endpoint, status=status_code).inc()
    http_request_duration_seconds.labels(method=method, endpoint=endpoint).observe(duration)


def record_prediction(sport: str, model_type: str, confidence: float):
    """Record prediction metrics"""
    predictions_total.labels(sport=sport, model_type=model_type).inc()
    prediction_confidence_avg.labels(sport=sport).set(confidence)


def record_cache_hit(cache_type: str = "redis"):
    """Record cache hit"""
    cache_hits_total.labels(cache_type=cache_type).inc()
    cache_operations_total.labels(operation="get", status="hit").inc()


def record_cache_miss(cache_type: str = "redis"):
    """Record cache miss"""
    cache_misses_total.labels(cache_type=cache_type).inc()
    cache_operations_total.labels(operation="get", status="miss").inc()


def record_cache_set(cache_type: str = "redis", success: bool = True):
    """Record cache set operation"""
    status = "success" if success else "error"
    cache_operations_total.labels(operation="set", status=status).inc()


def record_api_error(error_type: str, endpoint: str):
    """Record API error"""
    api_errors_total.labels(error_type=error_type, endpoint=endpoint).inc()


def record_db_query(operation: str, table: str, duration: float):
    """Record database query metrics"""
    db_queries_total.labels(operation=operation, table=table).inc()
    db_query_duration_seconds.labels(operation=operation, table=table).observe(duration)


def set_redis_status(connected: bool):
    """Set Redis connection status"""
    redis_connected.set(1 if connected else 0)


def get_metrics():
    """Get Prometheus metrics"""
    return generate_latest()


def metrics_response() -> Response:
    """Create FastAPI response with metrics"""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

