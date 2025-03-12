import os

class Conf:
    def __init__(self):
        self.mongo_url = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
        self.mongo_db =  os.environ.get("MONGO_DB", "db")
        self.mongo_collection = os.environ.get("MONGO_COLLECTION", "urls")
        self.short_url_length = int(os.environ.get("SHORT_URL_LENGTH", 10))
        
        


conf = Conf()