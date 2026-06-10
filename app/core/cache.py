import json
from typing import Optional, Any

try:
    import redis.asyncio as redis
    _redis_available = True
except ImportError:
    _redis_available = False


class CacheService:
    def __init__(self):
        self.client = None

    async def connect(self):
        if not _redis_available:
            return
        try:
            from app.core.config import settings
            self.client = await redis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
            )
        except Exception:
            self.client = None

    async def get(self, key: str) -> Optional[Any]:
        if self.client is None:
            await self.connect()
        if self.client is None:
            return None
        try:
            value = await self.client.get(key)
            if value:
                return json.loads(value)
        except Exception:
            pass
        return None

    async def set(self, key: str, value: Any, ttl: int = 300):
        if self.client is None:
            await self.connect()
        if self.client is None:
            return
        try:
            await self.client.setex(key, ttl, json.dumps(value))
        except Exception:
            pass

    async def delete(self, key: str):
        if self.client is None:
            await self.connect()
        if self.client is None:
            return
        try:
            await self.client.delete(key)
        except Exception:
            pass

    async def close(self):
        if self.client:
            try:
                await self.client.close()
            except Exception:
                pass

cache = CacheService()
