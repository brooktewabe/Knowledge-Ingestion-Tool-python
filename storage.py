from pymongo import MongoClient, errors
import logging
from config import MONGO_URI, MONGO_DB, MONGO_COLLECTION

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoStorage:
    def __init__(self):
        try:
            self.client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            self.db = self.client[MONGO_DB]
            self.collection = self.db[MONGO_COLLECTION]
            
            # Create a unique index on 'url' for deduplication
            self.collection.create_index("url", unique=True)
            logger.info("Connected to MongoDB.")
        except errors.ServerSelectionTimeoutError as e:
            logger.error(f"Could not connect to MongoDB: {e}")
            raise
        except Exception as e:
            logger.error(f"Error initializing storage: {e}")
            raise

    def save_page(self, page_data):
        """
        Saves page data to MongoDB. Returns True if saved, False if it was a duplicate.
        """
        try:
            self.collection.insert_one(page_data)
            logger.debug(f"Saved: {page_data.get('url')}")
            return True
        except errors.DuplicateKeyError:
            logger.debug(f"Skipped duplicate: {page_data.get('url')}")
            return False
        except Exception as e:
            logger.error(f"Error saving data: {e}")
            return False

    def is_already_ingested(self, url):
        """ Checks if a URL is already in the database. """
        return self.collection.find_one({"url": url}) is not None

    def close(self):
        self.client.close()
