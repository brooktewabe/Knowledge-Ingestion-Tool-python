import time
import logging
import argparse
import sys
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
    def __init__(self, urls=None):
        # Merge CLI URLs with defaults from config (CLI URLs priority)
        target_urls = list(urls) if urls else []
        # Add defaults if they aren't already in the list
        for url in INITIAL_URLS:
            if url not in target_urls:
                target_urls.append(url)
                
        self.queue = deque(target_urls)
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
    parser = argparse.ArgumentParser(description="Knowledge Ingestion Service Pipeline")
    parser.add_argument(
        "urls", 
        nargs="*", 
        help="Target Wikipedia URLs to ingest. If omitted, uses default list in config.py"
    )
    
    args = parser.parse_args()
    
    pipeline = IngestionPipeline(urls=args.urls)
    try:
        pipeline.run()
    except KeyboardInterrupt:
        logger.info("Pipeline interrupted by user.")
    except Exception as e:
        logger.error(f"Pipeline crashed: {e}")
