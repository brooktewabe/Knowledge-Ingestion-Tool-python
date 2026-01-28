import time
import logging
from collections import deque
from config import INITIAL_URLS, RATE_LIMIT_DELAY
from storage import MongoStorage
from ingestion import WikiIngestor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Pipeline")

class IngestionPipeline:
    def __init__(self):
        self.queue = deque(INITIAL_URLS)
        self.storage = MongoStorage()
        self.ingestor = WikiIngestor()
        self.processed_count = 0

    def run(self):
        logger.info(f"Starting pipeline with {len(self.queue)} initial URLs.")
        
        while self.queue:
            url = self.queue.popleft()
            
            # Deduplication check before fetching
            if self.storage.is_already_ingested(url):
                logger.info(f"Skipping already ingested URL: {url}")
                continue

            logger.info(f"Processing: {url}")
            
            # Rate Limiting
            time.sleep(RATE_LIMIT_DELAY)

            # Extraction
            html = self.ingestor.fetch_page(url)
            if not html:
                continue

            data = self.ingestor.extract_data(html, url)
            
            # Persistence & Final Deduplication
            success = self.storage.save_page(data)
            
            if success:
                self.processed_count += 1
                logger.info(f"Successfully ingested: {data['title']}")
            else:
                logger.warning(f"Failed to save data for {url} (possibly concurrent duplicate)")

        logger.info(f"Pipeline finished. Processed {self.processed_count} new pages.")
        self.storage.close()

if __name__ == "__main__":
    pipeline = IngestionPipeline()
    try:
        pipeline.run()
    except KeyboardInterrupt:
        logger.info("Pipeline interrupted by user.")
    except Exception as e:
        logger.error(f"Pipeline crashed: {e}")
