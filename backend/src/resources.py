import logging
from typing import Callable
import falcon
import falcon.asgi
import validators
from hashlib import shake_256
from pymongo.collection import Collection


# print(client.list_database_names())

logging.basicConfig(level=logging.INFO)


logger = logging.getLogger(__name__)






class LinkShortenResource:
    def __init__(self, collection: Collection, shorten_url: Callable[[str], str]):
        self.collection = collection
        self.shorten_url = shorten_url
    
    async def on_post(self, req, resp):
        long_url = (await req.media).get("url")
        if not long_url:
            resp.status = falcon.HTTP_400
            resp.media = {"error": "Missing or empty 'url' field"}
            return

        try:
            validators.url(long_url, r_ve=True)
        except validators.utils.ValidationError as e:
            resp.status = falcon.HTTP_400
            resp.media = {"error": str(e)}
            return 

        resp.status = falcon.HTTP_200
        short = self.shorten_url(long_url)
        short_url = f'{req.url.split("/")[2]}/r/{short}'
        found = self.collection.find_one({"short_url": short})
        if found:
            logger.info(f"Short URL {short} already exists")
        else:
            self.collection.insert_one(
                {
                    "short_url": short,
                    "long_url": long_url,
                    "ip": (
                        req.access_route[0]
                        if req.access_route
                        else req.remote_addr
                    ),
                    "user_agent": req.user_agent,
                    "count": 1,
                }
            )
        resp.media = {"url": long_url, "short_url": short_url}


class TelemetryResouce:
    def __init__(self, collection: Collection):
        self.collection = collection
        
    
    
    async def on_get_owner(self, req, resp, short_url):
        document = self.collection.find_one({"short_url": short_url})
        if document:
            resp.media = {"ip": document["ip"], "user_agent": document["user_agent"]}
        else:
            resp.status = falcon.HTTP_404
            resp.media = {"error": f"Short URL {short_url} not found"}

    async def on_get_count(self, req, resp, short_url):
        document = self.collection.find_one({"short_url": short_url})
        if document:
            resp.media = {"count": document["count"]}
        else:
            resp.status = falcon.HTTP_404
            resp.media = {"error": f"Short URL {short_url} not found"}


class RedirectResource:
    def __init__(self, collection: Collection):
        self.collection = collection
    
    
    async def on_get(self, req, resp, short_url):
        document = self.collection.find_one({"short_url": short_url})
        if document:
            result = self.collection.update_one({"short_url": short_url}, {"$inc": {"count": 1}})
            logger.info(f"Update result: {result.raw_result}")
            logger.info(f"Redirecting from {short_url} to {document['long_url']}")
            resp.status = falcon.HTTP_302
            resp.set_header("Location", document["long_url"])
        else:
            resp.status = falcon.HTTP_404
            resp.media = {"error": "URL not found"}



