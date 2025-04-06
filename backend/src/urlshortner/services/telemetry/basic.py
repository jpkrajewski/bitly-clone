import logging

from falcon import Request
from urlshortner.repositories.db.base import AbstractLinkRepository
from urlshortner.services.telemetry.base import AbstractTelemetryService, Owner

logger = logging.getLogger(__name__)


class BasicTelemetryService(AbstractTelemetryService):

    def __init__(self, repository: AbstractLinkRepository):
        self.repository = repository

    def get_owner(self, short_url: str, req: Request) -> None | Owner:
        doc = self.repository.get_by_short(short_url)
        if not doc:
            logger.warning(f"No document found for short_url={short_url}")
            return None
        return Owner(ip=doc.ip, user_agent=doc.user_agent)

    def get_link_count(self, short_url: str) -> None | int:
        doc = self.repository.get_by_short(short_url)
        if not doc:
            logger.warning(f"No document found for short_url={short_url}")
            return None
        return doc.count
