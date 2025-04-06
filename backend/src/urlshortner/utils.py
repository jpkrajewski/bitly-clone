from hashlib import shake_256

from falcon import HTTP_404, Response
from urlshortner.conf import conf


def shorten_url(url: str) -> str:
    return shake_256(url.encode()).hexdigest(conf.short_url_length)


def response_404(response: Response, message: str) -> None:
    response.media = {"error": message}
    response.status = HTTP_404
