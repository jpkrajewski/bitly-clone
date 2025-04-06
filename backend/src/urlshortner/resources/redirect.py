import logging

import falcon
from falcon import Request, Response
from urlshortner.services.link.base import AbstractLinkService
from urlshortner.utils import response_404

logger = logging.getLogger(__name__)


def response_302(resp: Response, resolved_url: str):
    resp.status = falcon.HTTP_302
    resp.set_headers({"Location": resolved_url, "Cache-Control": "no-store"})


class RedirectResource:

    def __init__(self, link_service: AbstractLinkService):
        self.link_service = link_service

    async def on_get(self, req: Request, resp: Response, short_url: str):
        if resolved_url := self.link_service.resolve(short_url):
            response_302(resp, resolved_url)
        else:
            response_404(resp, "URL not found")
