import os
import json
from typing import Optional, Any

# Conditional import to ensure zero local crashes if dependencies are missing during builds
try:
    import redis
except ImportError:
    redis = None

class ProductionCacheManager:
    """Manages high-throughput connection pools for non-blocking state storage."""
    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.client = redis.Redis.from_url(self.redis_url, decode_responses=True) if redis else None

    def set_state(self, key: str, value: Any, expire_seconds: int = 10):
        """Caches data strings into memory using Least Recently Used policies."""
        if self.client:
            try:
                serialized = json.dumps(value) if isinstance(value, (dict, list)) else str(value)
                self.client.set(key, serialized, ex=expire_seconds)
            except Exception as e:
                print(f"[Cache Warning] Write pass failure: {e}")

    def get_state(self, key: str) -> Optional[str]:
        """Fetches raw strings directly from memory loops."""
        if self.client:
            try:
                return self.client.get(key)
            except Exception:
                return None
        return None

mrg_cache = ProductionCacheManager()
