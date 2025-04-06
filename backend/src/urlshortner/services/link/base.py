from abc import ABC, abstractmethod
from dataclasses import dataclass

from falcon import Request


@dataclass
class ShortLongUrlDTO:
    long: str
    short: str


class AbstractLinkService(ABC):

    @abstractmethod
    def shorten(self, long_url: str, req: Request) -> ShortLongUrlDTO:
        pass

    @abstractmethod
    def resolve(self, short_url: str) -> None | str:
        pass
