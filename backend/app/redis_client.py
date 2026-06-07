import json
from typing import Any

import redis.asyncio as redis

from app.config import settings

redis_client: redis.Redis | None = None


async def connect_redis() -> None:
    global redis_client
    redis_client = redis.from_url(settings.redis_url, decode_responses=True)


async def close_redis() -> None:
    global redis_client
    if redis_client:
        await redis_client.close()
    redis_client = None


def get_redis() -> redis.Redis:
    if redis_client is None:
        raise RuntimeError("Redis not initialized")
    return redis_client


async def cache_get(key: str) -> Any | None:
    value = await get_redis().get(key)
    if value is None:
        return None
    return json.loads(value)


async def cache_set(key: str, value: Any, ttl: int = 300) -> None:
    await get_redis().set(key, json.dumps(value), ex=ttl)


async def cache_delete(key: str) -> None:
    await get_redis().delete(key)
