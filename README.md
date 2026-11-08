# Tech Hardware Price Monitor (ETL Pipeline)

An automated Data Engineering pipeline that extracts hardware prices from an e-commerce platform, processes the data through a local SQLite database, enriches it with live foreign exchange rates, and generates a formatted, client-ready Excel dashboard.

## 🚀 System Architecture

This project follows a modular, microservice-style architecture separated into distinct logical steps:

1. **Extraction (`scraper.py`)**: Utilizes `requests` and `BeautifulSoup4` to parse HTML. Implements randomized request delays (`time.sleep`) to mimic human behavior and avoid rate-limiting/IP bans while looping through multiple product categories (Laptops, Tablets, Phones).
2. **Database & Storage (`database.py`)**: Manages a local `SQLite3` database. Utilizes strict `UNIQUE` constraints and `UPSERT` (Update or Insert) logic to prevent data duplication and maintain historical price accuracy on daily runs.
3. **API Enrichment (`api_enricher.py`)**: Connects to a live REST API (ExchangeRate-API) to fetch current market currency conversion rates (USD to EUR and GBP).
4. **Data Transformation & Export (`exporter.py`)**: Uses `Pandas` to clean strings into native floats and calculate currency conversions. Leverages `OpenPyXL` to split the data into dynamic category sheets, auto-adjust column widths, and apply native Excel currency formatting.
5. **Orchestration (`main.py`)**: The central controller that coordinates the flow of data between the modules.

## 🛠️ Technology Stack
* **Language:** Python 3
* **Web Scraping:** BeautifulSoup4, Requests
* **Database:** SQLite3 (Native Python)
* **Data Manipulation:** Pandas
* **Reporting:** OpenPyXL
* **Version Control:** Git / GitHub

## 📊 Business Value

This pipeline demonstrates how to solve the classic "E-Commerce Competitor Monitoring" problem. Instead of relying on manual data entry, the script automates the ingestion of hundreds of SKUs, normalizes the data, completely prevents duplicate records via SQL constraints, and outputs a formatted multi-sheet `.xlsx` report that business stakeholders can immediately use for pricing strategy.

## ⚙️ How to Run

1. Clone the repository and navigate to the project folder.
2. Activate your virtual environment: `.\venv\Scripts\Activate`
3. Install the required dependencies: `pip install -r requirements.txt`
4. Run the orchestrator: `python main.py`

The pipeline will execute, and the final multi-sheet report will be saved inside the automatically generated `report/` directory.