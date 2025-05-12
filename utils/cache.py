import json
import logging
import os
from typing import Optional

from redis.asyncio import Redis

class CacheManager:
    def __init__(self, redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")):
        self.redis_url = redis_url
        self.ttl = int(os.getenv("TTL", "86400"))
        self.redis: Optional[Redis] = None

    async def initialize(self):
        self.redis = Redis.from_url(self.redis_url, decode_responses = True)

    async def set(self, key: str, value: str):
        try:
            await self.redis.set(key, value, self.ttl)
            print("Value successfully set in redis")
            return True

        except Exception as e:
            logging.error(f"Error setting cache in redis: {e}")
            return False
        
    async def get(self, key: str):
        try:
            value = await self.redis.get(key)
            print(f"Value successfully get in redis: {value}")

            if value is not None:
                return json.loads(value)
            
            return None

        except Exception as e:
            logging.error(f"Error in getting the cache: {e}")
            return None
        
cache_manager = CacheManager()