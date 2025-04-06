from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict


@dataclass
class LinkDTO:
    short_url: str
    long_url: str
    count: int
    ip: str
    user_agent: str

    def to_dict(self) -> dict:
        return asdict(self)


class AbstractLinkRepository(ABC):

    @abstractmethod
    def get_by_short(self, short: str) -> None | LinkDTO:
        pass

    @abstractmethod
    def save_shortened_url(self, short: str, long_url: str, ip: str,
                           user_agent: str) -> None:
        pass

    @abstractmethod
    def increment_counter(self, short: str) -> None:
        pass
