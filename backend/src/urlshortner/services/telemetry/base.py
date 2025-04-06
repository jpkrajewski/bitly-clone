from abc import ABC, abstractmethod
from dataclasses import dataclass

from falcon import Request


@dataclass
class Owner:
    ip: str
    user_agent: str


class AbstractTelemetryService(ABC):

    @abstractmethod
    def get_owner(self, short_url: str, req: Request) -> None | Owner:
        pass

    @abstractmethod
    def get_link_count(self, short_url: str) -> None | int:
        pass
