"""
Redis caching layer for API efficiency
"""
import redis
import json
import pickle
from typing import Optional, Any, Union
from functools import wraps
from datetime import timedelta
from app.config import settings
import hashlib


class RedisCache:
    """Redis cache manager"""
    
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0, decode_responses: bool = False):
        """
        Initialize Redis connection
        
        Args:
            host: Redis host
            port: Redis port
            db: Redis database number
            decode_responses: Whether to decode responses as strings
        """
        try:
            self.redis_client = redis.Redis(
                host=host,
                port=port,
                db=db,
                decode_responses=decode_responses,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            # Test connection
            self.redis_client.ping()
            self.enabled = True
        except (redis.ConnectionError, redis.TimeoutError) as e:
            print(f"Redis connection failed: {e}. Caching disabled.")
            self.redis_client = None
            self.enabled = False
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache
        
        Args:
            key: Cache key
        
        Returns:
            Cached value or None
        """
        if not self.enabled:
            return None
        
        try:
            value = self.redis_client.get(key)
            if value:
                # Try to deserialize
                try:
                    return pickle.loads(value)
                except:
                    # Fallback to JSON
                    try:
                        return json.loads(value)
                    except:
                        return value
            return None
        except Exception as e:
            print(f"Redis get error: {e}")
            return None
    
    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """
        Set value in cache
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds
        
        Returns:
            True if successful
        """
        if not self.enabled:
            return False
        
        try:
            # Serialize value
            try:
                serialized = pickle.dumps(value)
            except:
                serialized = json.dumps(value).encode('utf-8')
            
            if ttl:
                return self.redis_client.setex(key, ttl, serialized)
            else:
                return self.redis_client.set(key, serialized)
        except Exception as e:
            print(f"Redis set error: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if not self.enabled:
            return False
        
        try:
            return bool(self.redis_client.delete(key))
        except Exception as e:
            print(f"Redis delete error: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists"""
        if not self.enabled:
            return False
        
        try:
            return bool(self.redis_client.exists(key))
        except Exception as e:
            print(f"Redis exists error: {e}")
            return False
    
    def clear_pattern(self, pattern: str) -> int:
        """Clear all keys matching pattern"""
        if not self.enabled:
            return 0
        
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                return self.redis_client.delete(*keys)
            return 0
        except Exception as e:
            print(f"Redis clear_pattern error: {e}")
            return 0


# Global cache instance
_cache_instance: Optional[RedisCache] = None


def get_cache() -> RedisCache:
    """Get or create cache instance"""
    global _cache_instance
    if _cache_instance is None:
        # Try to get from environment or use defaults
        redis_host = getattr(settings, 'REDIS_HOST', 'localhost')
        redis_port = getattr(settings, 'REDIS_PORT', 6379)
        redis_db = getattr(settings, 'REDIS_DB', 0)
        _cache_instance = RedisCache(host=redis_host, port=redis_port, db=redis_db)
    return _cache_instance


def cache_key(*args, **kwargs) -> str:
    """Generate cache key from arguments"""
    key_parts = []
    for arg in args:
        if isinstance(arg, (dict, list)):
            key_parts.append(json.dumps(arg, sort_keys=True))
        else:
            key_parts.append(str(arg))
    
    for k, v in sorted(kwargs.items()):
        if isinstance(v, (dict, list)):
            key_parts.append(f"{k}:{json.dumps(v, sort_keys=True)}")
        else:
            key_parts.append(f"{k}:{v}")
    
    key_string = "|".join(key_parts)
    return hashlib.md5(key_string.encode()).hexdigest()


def cached(ttl: int = 300, key_prefix: str = ""):
    """
    Decorator to cache function results
    
    Args:
        ttl: Time to live in seconds
        key_prefix: Prefix for cache key
    """
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            cache = get_cache()
            if not cache.enabled:
                return await func(*args, **kwargs)
            
            # Generate cache key
            cache_key_str = f"{key_prefix}:{func.__name__}:{cache_key(*args, **kwargs)}"
            
            # Try to get from cache
            cached_value = cache.get(cache_key_str)
            if cached_value is not None:
                return cached_value
            
            # Call function and cache result
            result = await func(*args, **kwargs)
            cache.set(cache_key_str, result, ttl=ttl)
            return result
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            cache = get_cache()
            if not cache.enabled:
                return func(*args, **kwargs)
            
            # Generate cache key
            cache_key_str = f"{key_prefix}:{func.__name__}:{cache_key(*args, **kwargs)}"
            
            # Try to get from cache
            cached_value = cache.get(cache_key_str)
            if cached_value is not None:
                return cached_value
            
            # Call function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key_str, result, ttl=ttl)
            return result
        
        # Return appropriate wrapper
        import inspect
        if inspect.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator

