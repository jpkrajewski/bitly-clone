from urlshortner.repositories.db.base import AbstractLinkRepository, LinkDTO


class MemoryLinkRepository(AbstractLinkRepository):

    def __init__(self):
        self.store = {}

    def get_by_short(self, short: str) -> None | LinkDTO:
        if link := self.store.get(short):
            return LinkDTO(**link)
        return None

    def save_shortened_url(self, short: str, long_url: str, ip: str,
                           user_agent: str) -> None:
        self.store[short] = {
            "short_url": short,
            "long_url": long_url,
            "ip": ip,
            "user_agent": user_agent,
            "count": 0,
        }

    def increment_counter(self, short: str) -> None:
        if short in self.store:
            self.store[short]["count"] += 1
