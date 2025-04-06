from urlshortner.repositories.cache.base import AbstractCacheRepository
from urlshortner.repositories.db.base import AbstractLinkRepository, LinkDTO


class CachedLinkRepository(AbstractLinkRepository):

    def __init__(
        self,
        link_repository: AbstractLinkRepository,
        cache_repository: AbstractCacheRepository,
    ):
        self.link_repository = link_repository
        self.cache_repository = cache_repository

    def get_by_short(self, short: str) -> None | LinkDTO:
        cached = self.cache_repository.get(short)
        if cached:
            return LinkDTO(**cached)

        link = self.link_repository.get_by_short(short)
        if link:
            self.cache_repository.set(short, link.to_dict())
        return link

    def save_shortened_url(self, short: str, long_url: str, ip: str,
                           user_agent: str) -> None:
        self.link_repository.save_shortened_url(short, long_url, ip, user_agent)
        self.cache_repository.set(
            short, {
                "short_url": short,
                "long_url": long_url,
                "ip": ip,
                "user_agent": user_agent,
                "count": 0,
            })

    def increment_counter(self, short: str) -> None:
        self.link_repository.increment_counter(short)
        self.cache_repository.invalidate(short)
