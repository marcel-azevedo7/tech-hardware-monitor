# 🖥️ Tech Hardware Price Monitor & ETL Pipeline

An automated Web Scraping and ETL (Extract, Transform, Load) pipeline that tracks international tech hardware prices, enriches them with live currency API data, and maintains a persistent historical database.

## 🚀 Project Overview
This project demonstrates end-to-end data automation. It safely extracts live product data from the web, processes the information, tracks price changes over time using a relational database, and automatically generates a business-ready Excel dashboard. 

**Key Capabilities:**
- **Automated Web Scraping:** Extracts product names, specifications, and current USD prices using `requests` and `BeautifulSoup`.
- **Live API Integration:** Fetches real-time exchange rates (USD to EUR/GBP) via REST API to dynamically enrich the scraped dataset.
- **Relational Data Persistence:** Uses `SQLite` to store historical pricing, allowing the system to identify if a price has dropped or increased since the last run.
- **Automated Reporting:** Leverages `Pandas` and `OpenPyXL` to clean the data and export a formatted, timestamped `.xlsx` ledger.

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **Data Extraction:** `BeautifulSoup4`, `requests`
- **Data Transformation:** `Pandas`, JSON API parsing
- **Database:** `SQLite`
- **Reporting:** `OpenPyXL`

## 🧠 Engineering Highlights
- Modular architecture separating the scraper, API handler, database controller, and exporter.
- Robust HTTP error handling and status code validation.
- SQL logic designed for UPSERT operations (inserting new products or updating existing ones).