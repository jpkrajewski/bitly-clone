from typing import Tuple
import falcon.asgi
from pymongo import MongoClient
from redis import Redis
from urlshortner.conf import conf
from urlshortner.repositories import (AbstractLinkRepository,
                                      MemoryLinkRepository, MongoLinkRepository,
                                      MemoryCacheRepository,
                                      RedisCacheRepository,
                                      AbstractCacheRepository)
from urlshortner.resources import (LinkShortenResource, RedirectResource,
                                   TelemetryResouce)
from urlshortner.services.link.basic import BasicLinkService
from urlshortner.services.telemetry.basic import BasicTelemetryService
from urlshortner.utils import shorten_url
from urlshortner.cached_repositories.link import CachedLinkRepository
import logging

logger = logging.getLogger(__name__)


def get_repository() -> AbstractLinkRepository:
    if conf.repository_db_type == "mongo":
        client = MongoClient(conf.mongo_url)
        db = client[conf.mongo_db]
        return MongoLinkRepository(db[conf.mongo_collection])
    elif conf.repository_db_type == "memory":
        return MemoryLinkRepository()
    raise ValueError(
        f"Unknown repository type: {conf.repository_db_type}, please setup enviroment variable URLSHORT_REPO_DB_TYPE"
    )


def cached_repository_wrapper(
        repository: AbstractLinkRepository) -> CachedLinkRepository:
    cache_repository: AbstractCacheRepository
    if conf.repository_cache_type == "memory":
        cache_repository = MemoryCacheRepository()
    elif conf.repository_cache_type == "redis":
        redis = Redis(host=conf.redis_host,
                      port=conf.redis_port,
                      db=conf.redis_db,
                      username=conf.redis_username,
                      password=conf.redis_password,
                      ssl=conf.redis_ssl)
        if not redis.ping():
            logger.error(f"Redis ping failed")
        cache_repository = RedisCacheRepository(redis)
    else:
        raise ValueError(
            f"Unknown repository type: {conf.repository_db_type}, please setup enviroment variable URLSHORT_REPO_CACHE_TYPE"
        )
    return CachedLinkRepository(link_repository=repository,
                                cache_repository=cache_repository)


def create_services(
    repository: AbstractLinkRepository
) -> Tuple[BasicLinkService, BasicTelemetryService]:
    link_service = BasicLinkService(repository, shorten_url)
    telemetry_service = BasicTelemetryService(repository)
    return link_service, telemetry_service


def configure_routes(app: falcon.asgi.App, link_service,
                     telemetry_service) -> None:
    app.add_route("/shorten", LinkShortenResource(link_service))
    app.add_route("/r/{short_url}", RedirectResource(link_service))
    app.add_route("/telemetry/count/{short_url}",
                  TelemetryResouce(telemetry_service),
                  suffix="count")
    app.add_route("/telemetry/owner/{short_url}",
                  TelemetryResouce(telemetry_service),
                  suffix="owner")


def create_app() -> falcon.asgi.App:
    repository = cached_repository_wrapper(get_repository())
    link_service, telemetry_service = create_services(repository)

    app = falcon.asgi.App()
    configure_routes(app, link_service, telemetry_service)
    return app


app = create_app()
