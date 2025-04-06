import logging

import falcon
import validators
from falcon import Request, Response
from urlshortner.services.link.base import AbstractLinkService
from urlshortner.utils import response_404

logger = logging.getLogger(__name__)


class LinkShortenResource:

    def __init__(self, link_service: AbstractLinkService):
        self.link_service = link_service

    async def on_post(self, req: Request, resp: Response):
        long_url = (await req.media).get("url")
        if not long_url:
            response_404(resp, "Missing or empty 'url' field")
            return

        try:
            validators.url(long_url, r_ve=True)
        except validators.utils.ValidationError as e:
            resp.status = falcon.HTTP_400
            resp.media = {"error": str(e)}
            return

        result = self.link_service.shorten(long_url, req)
        resp.status = falcon.HTTP_200
        resp.media = {"url": result.long, "short_url": result.short}
