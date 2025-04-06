import os
from typing import Literal


class Conf:

    def __init__(self):
        # MongoDB configurations
        self.mongo_url = os.environ.get("URLSHORT_MONGO_URI",
                                        "mongodb://localhost:27017")
        self.mongo_db = os.environ.get("URLSHORT_MONGO_DB", "db")
        self.mongo_collection = os.environ.get("URLSHORT_MONGO_COLLECTION",
                                               "urls")

        # Application configurations
        self.short_url_length = int(
            os.environ.get("URLSHORT_SHORT_URL_LENGTH", 10))
        self.repository_db_type: Literal["memory", "mongo"] = os.environ.get(
            "URLSHORT_REPO_DB_TYPE", "memory")
        self.repository_cache_type: Literal["memory", "redis"] = os.environ.get(
            "URLSHORT_REPO_CACHE_TYPE", "memory")

        # Redis configurations
        self.redis_host = os.environ.get("URLSHORT_REDIS_HOST", "localhost")
        self.redis_port = int(os.environ.get("URLSHORT_REDIS_PORT", 6379))
        self.redis_db = int(os.environ.get("URLSHORT_REDIS_DB", 0))
        self.redis_username = os.environ.get("URLSHORT_REDIS_USERNAME", None)
        self.redis_password = os.environ.get("URLSHORT_REDIS_PASSWORD", None)
        self.redis_ssl = os.environ.get("URLSHORT_REDIS_SSL",
                                        "false").lower() in ("true", "1", "t")


conf = Conf()
