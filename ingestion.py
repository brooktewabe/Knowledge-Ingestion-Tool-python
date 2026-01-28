import requests
from bs4 import BeautifulSoup
import logging
import time
from datetime import datetime

logger = logging.getLogger(__name__)

class WikiIngestor:
    def __init__(self, user_agent="KnowledgeIngestionBot/1.0"):
        self.headers = {"User-Agent": user_agent}

    def fetch_page(self, url):
        """Fetches the page content safely."""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    def extract_data(self, html, url):
        """Extracts structured data from Wikipedia HTML."""
        if not html:
            return None

        soup = BeautifulSoup(html, 'html.parser')
        
        # Title
        title = soup.find(id="firstHeading")
        title_text = title.get_text() if title else "Unknown Title"

        # Summary (first non-empty paragraph)
        ###=============================================###
        # TODO: add more complex summary extraction logic like using NLP to extract the main points
        ###=============================================###
        summary = ""
        content_div = soup.find(id="mw-content-text")
        if content_div:
            # Look for paragraphs that are direct children of the parser output
            paras = content_div.find_all('p', recursive=True)
            for p in paras:
                text = p.get_text().strip()
                if text:
                    summary = text
                    break

        # Tables
        tables_data = []
        tables = soup.find_all('table', class_='wikitable')
        for idx, table in enumerate(tables):
            headers = [th.get_text().strip() for th in table.find_all('th')]
            rows = []
            for tr in table.find_all('tr')[1:]: # Skip header row
                cells = [td.get_text().strip() for td in tr.find_all('td')]
                if cells:
                    # Map to headers if count matches, otherwise just store cells
                    if len(cells) == len(headers):
                        rows.append(dict(zip(headers, cells)))
                    else:
                        rows.append(cells)
            
            if rows:
                tables_data.append({
                    "table_index": idx,
                    "row_count": len(rows),
                    "data": rows
                })

        return {
            "url": url,
            "title": title_text,
            "summary": summary,
            "tables": tables_data,
            "ingested_at": datetime.utcnow().isoformat()
        }
