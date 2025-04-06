from pymongo.collection import Collection
from urlshortner.repositories.db.base import AbstractLinkRepository, LinkDTO


class MongoLinkRepository(AbstractLinkRepository):

    def __init__(self, collection: Collection):
        self.collection = collection

    def get_by_short(self, short: str) -> None | LinkDTO:
        if link := self.collection.find_one({"short_url": short}):
            return LinkDTO(**link)
        return None

    def save_shortened_url(self, short: str, long_url: str, ip: str,
                           user_agent: str) -> None:
        self.collection.insert_one({
            "short_url": short,
            "long_url": long_url,
            "ip": ip,
            "user_agent": user_agent,
            "count": 0,
        })

    def increment_counter(self, short: str) -> None:
        self.collection.update_one({"short_url": short}, {"$inc": {"count": 1}})
