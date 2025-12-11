"""
Middleware for monitoring and metrics
"""
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import time
from app.monitoring.prometheus_metrics import (
    record_request,
    record_api_error,
    active_connections
)


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware to collect HTTP metrics"""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Increment active connections
        active_connections.inc()
        
        try:
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Extract endpoint (simplified)
            endpoint = request.url.path
            if endpoint.startswith("/api/"):
                # Extract main endpoint
                parts = endpoint.split("/")
                if len(parts) >= 3:
                    endpoint = f"/api/{parts[2]}"
            
            # Record metrics
            record_request(
                method=request.method,
                endpoint=endpoint,
                status_code=response.status_code,
                duration=duration
            )
            
            # Record errors
            if response.status_code >= 400:
                error_type = "client_error" if response.status_code < 500 else "server_error"
                record_api_error(error_type, endpoint)
            
            return response
        
        except Exception as e:
            # Record exception
            duration = time.time() - start_time
            endpoint = request.url.path
            record_api_error("exception", endpoint)
            raise
        
        finally:
            # Decrement active connections
            active_connections.dec()

