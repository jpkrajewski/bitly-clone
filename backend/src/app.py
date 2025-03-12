import pymongo.collection
from src.resources import LinkShortenResource, RedirectResource, TelemetryResouce
import falcon.asgi
import pymongo
from src.utils import shorten_url
from src.conf import conf
from pymongo.collection import Collection

def create_app(collection: Collection) -> falcon.asgi.App:
    telemetry = TelemetryResouce(collection)

    app = falcon.asgi.App()
    app.add_route("/shorten", LinkShortenResource(collection, shorten_url))
    app.add_route("/r/{short_url}", RedirectResource(collection))
    app.add_route("/telemetry/count/{short_url}", telemetry, suffix="count")
    app.add_route("/telemetry/owner/{short_url}", telemetry, suffix="owner")

    return app


client = pymongo.MongoClient(conf.mongo_url)
database = client[conf.mongo_db]
collection = database[conf.mongo_collection]
app = create_app(collection)