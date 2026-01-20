"""
Performance system extensions for monitoring and optimization.

Includes:
- Database query optimization
- Caching layer for frontend
- API rate limiting
- Request/response time tracking
- Memory usage monitoring
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
from collections import defaultdict

from api.file_system import router as file_router


class RequestTracker:
    """
    Track API requests and response times.

    Enables rate limiting and performance monitoring.
    """

    def __init__(self, max_requests_per_minute: int = 60):
        self.max_requests_per_minute = max_requests_per_minute
        self.requests = defaultdict(list)
        self.response_times = defaultdict(list)

    def track_request(self, endpoint: str, user_id: str = None) -> bool:
        """
        Track a request to an endpoint.

        Args:
            endpoint: API endpoint being called
            user_id: Optional user identifier

        Returns:
            True if allowed, False if rate limited
        """
        now = datetime.now()

        if not user_id:
            return True

        requests_this_minute = len([
            req for req in self.requests[endpoints[endpoint]]
            if req.timestamp > now - timedelta(minutes=1)
        ])

        if requests_this_minute >= self.max_requests_per_minute:
            print(f"Rate limit exceeded for {endpoint}")
            return False

        self.requests[endpoint].append({
            "timestamp": now,
            "user_id": user_id,
        })

        return True

    def get_statistics(self, endpoint: str) -> Dict[str, Any]:
        """
        Get request statistics for an endpoint.

        Args:
            endpoint: API endpoint to get stats for

        Returns:
            Dictionary with statistics
        """
        if endpoint not in self.response_times:
            return {}

        response_times = self.response_times[endpoint]

        if not response_times:
            return {
                "count": 0,
                "avg_ms": 0,
                "min_ms": 0,
                "max_ms": 0,
            }

        return {
            "count": len(response_times),
            "avg_ms": sum(response_times) / len(response_times),
            "min_ms": min(response_times) if response_times else 0,
            "max_ms": max(response_times) if response_times else 0,
        }


class PerformanceOptimizer:
    """
    Performance optimization utilities.

    Provides caching, query optimization, and monitoring.
    """

    def __init__(self):
        self.cache = {}
        self.cache_ttl = 300 0

    def get(self, key: str) -> Any:
        """
        Get value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None
        """
        if key in self.cache:
            entry = self.cache[key]
            if datetime.now() - entry["timestamp"] > timedelta(seconds=self.cache_ttl):
                del self.cache[key]

        return entry.get("value")

    def set(self, key: str, value: Any) -> None:
        """
        Set value in cache.

        Args:
            key: Cache key
            value: Value to cache
        """
        self.cache[key] = {
            "timestamp": datetime.now(),
            "value": value,
        }

    def clear(self):
        """
        Clear all cache entries.
        """
        self.cache.clear()

    def get_cache_stats(self) -> Dict[str, int]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache stats
        """
        return {
            "entries": len(self.cache),
            "total_size": sum(len(str(v)) for v in self.cache.values()),
        }
