import scraper
import database

TARGET_URL = "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops"

def main():
    print("Starting Tech Hardware Price Monitor...\n")
    
    # Step 1: Ensure the database and tables are ready
    print("--- Step 1: Initializing Database ---")
    database.setup_database()
    
    # Step 2: Scrape the data from the web
    print("\n--- Step 2: Scraping Web Data ---")
    print(f"Fetching data from: {TARGET_URL}")
    page_soup = scraper.fetch_html(TARGET_URL)
    
    if not page_soup:
        print("Failed to retrieve the webpage. Exiting pipeline.")
        return

    # Step 3: Extract the specific laptop information
    print("\n--- Step 3: Extracting Product Data ---")
    laptops_data = scraper.extract_laptop_data(page_soup)
    
    if not laptops_data:
        print("No laptop data found on the page. Exiting pipeline.")
        return
        
    # Step 4: Save the data using our UPSERT logic
    print("\n--- Step 4: Saving to Database ---")
    database.save_to_database(laptops_data)
    
    print("\nPipeline execution completed successfully!")

if __name__ == "__main__":
    main()