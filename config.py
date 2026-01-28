import os

# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB = "knowledge_ingestion"
MONGO_COLLECTION = "wikipedia_pages"

# Pipeline Configuration
RATE_LIMIT_DELAY = 1.0  # Seconds between requests
MAX_RETRIES = 3

# Target Wikipedia URLs for initial ingestion
INITIAL_URLS = [
    "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "https://en.wikipedia.org/wiki/Machine_learning",
    "https://en.wikipedia.org/wiki/Data_science",
    "https://en.wikipedia.org/wiki/Python_(programming_language)",
    "https://en.wikipedia.org/wiki/Web_scraping"
]
