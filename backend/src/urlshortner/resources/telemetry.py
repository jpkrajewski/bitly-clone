import logging

from falcon import Request, Response
from urlshortner.services.telemetry.base import AbstractTelemetryService
from urlshortner.utils import response_404

logger = logging.getLogger(__name__)


class TelemetryResouce:

    def __init__(self, telemetry_service: AbstractTelemetryService):
        self.telemetry_service = telemetry_service

    async def on_get_owner(self, req: Request, resp: Response, short_url: str):
        if owner := self.telemetry_service.get_owner(short_url, req):
            resp.media = {"ip": owner.ip, "user_agent": owner.user_agent}
        else:
            response_404(resp, f"Short URL {short_url} not found")

    async def on_get_count(self, req: Request, resp: Response, short_url: str):
        if (count :=
                self.telemetry_service.get_link_count(short_url)) is not None:
            resp.media = {"count": count}
        else:
            response_404(resp, f"Short URL {short_url} not found")
