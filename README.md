# Knowledge Ingestion Service (Wikipedia)

A professional-grade data ingestion pipeline designed to fetch, extract, and persist structured knowledge from Wikipedia at scale.

## 🚀 Key Features
- **Rate Limiting**: Intelligent delays between requests to respect robots.txt and prevent IP bans.
- **Job Queue**: Managed processing of target URLs using an asynchronous-ready architecture.
- **Deduplication**: MongoDB unique index enforcement to ensure data integrity and zero redundancy.
- **Structured Storage**: Extraction of titles, summaries, and complex tables into a document-oriented database.
- **Resilience**: Robust error handling and logging for production stability.

## 🏛️ Architecture
The service is built with modularity in mind:
- `pipeline.py`: Orchestrates the ingestion flow.
- `ingestion.py`: Contains the logic for BeautifulSoup parsing and cleaning.
- `storage.py`: Manages the connection and operations with MongoDB.
- `config.py`: Centralized configuration for easy deployment.

## 🛠️ Tech Stack
- **Language**: Python 3.x
- **Parsing**: BeautifulSoup4, Requests
- **Database**: MongoDB (via Pymongo)
- **Logging**: Python Standard Logging

## 🏁 Getting Started

### Prerequisites
- **MongoDB**: Ensure you have MongoDB installed and running locally (`mongodb://localhost:27017`).
- **Python**: Version 3.8 or higher.

### Installation
1. Clone the repository and navigate to the project directory.
2. Install the required dependencies:
   ```bash
   pip install pymongo requests beautifulsoup4
   ```

## 🚀 Usage
1. Configure your target URLs or database settings in `config.py` (optional), you could also modify it to accept a list of URLs as a command line argument.
2. Start the ingestion pipeline:
   ```bash
   python pipeline.py
   ```
3. The service will fetch the pages, apply rate limiting, and store the structured data in MongoDB while automatically handling duplicates.

## 📚 Why is this better than a simple scraper?
Check out [challenges.md](challenges.md) for a deep dive into the complexities of scraping at scale and how this service addresses them.

