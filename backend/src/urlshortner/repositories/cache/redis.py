from .base import AbstractCacheRepository
from redis import Redis


class RedisCacheRepository(AbstractCacheRepository):

    def __init__(self, redis: Redis):
        self.redis = redis

    def set(self, key: str, value: dict) -> None:
        self.redis.hset(key, mapping=value)

    def get(self, key: str) -> dict | None:
        if result := self.redis.hgetall(key):
            return result
        return None

    def invalidate(self, key: str) -> None:
        self.redis.delete(key)
