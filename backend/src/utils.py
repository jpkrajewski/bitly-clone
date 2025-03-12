from hashlib import shake_256
from src.conf import conf

def shorten_url(url: str) -> str:
    return shake_256(url.encode()).hexdigest(conf.short_url_length)