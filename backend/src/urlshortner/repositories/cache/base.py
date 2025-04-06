from abc import ABC, abstractmethod


class AbstractCacheRepository(ABC):

    @abstractmethod
    def set(self, key: str, value: dict) -> None:
        pass

    @abstractmethod
    def get(self, key: str) -> dict | None:
        pass

    @abstractmethod
    def invalidate(self, key: str) -> None:
        pass
