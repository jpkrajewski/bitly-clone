import logging
from dataclasses import dataclass
from typing import Callable
from urllib.parse import urlparse

from falcon import Request
from urlshortner.repositories.db.base import AbstractLinkRepository
from urlshortner.services.link.base import AbstractLinkService, ShortLongUrlDTO

logger = logging.getLogger(__name__)


class BasicLinkService(AbstractLinkService):

    def __init__(self, repository: AbstractLinkRepository,
                 shorten_url: Callable[[str], str]):
        self.repository = repository
        self.shorten_url = shorten_url

    def shorten(self, long_url: str, req: Request) -> ShortLongUrlDTO:
        short = self.shorten_url(long_url)
        parsed = urlparse(req.url)
        short_url = f'{parsed.scheme}://{parsed.netloc}/r/{short}'
        found = self.repository.get_by_short(short)
        if not found:
            self.repository.save_shortened_url(
                short=short,
                long_url=long_url,
                ip=req.access_route[0] if req.access_route else req.remote_addr,
                user_agent=req.user_agent,
            )
        return ShortLongUrlDTO(long=long_url, short=short_url)

    def resolve(self, short_url: str) -> None | str:
        doc = self.repository.get_by_short(short_url)
        if doc:
            self.repository.increment_counter(short_url)
            return doc.long_url
        return None
