from .base import AbstractCacheRepository


class MemoryCacheRepository(AbstractCacheRepository):

    def __init__(self):
        self.store = {}

    def set(self, key: str, value: dict) -> None:
        self.store[key] = value

    def get(self, key: str) -> dict | None:
        return self.store.get(key)

    def invalidate(self, key: str):
        if key in self.store:
            del self.store[key]
