import scraper
import database
import exporter
import time
import random

# Dictionary mapping our categories to their exact URLs
TARGET_URLS = {
    "Laptops": "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops",
    "Tablets": "https://webscraper.io/test-sites/e-commerce/allinone/computers/tablets",
    "Phones": "https://webscraper.io/test-sites/e-commerce/allinone/phones/touch"
}

def main():
    print("Starting Multi-Category Hardware Price Monitor...\n")
    
    print("--- Step 1: Initializing Database ---")
    database.setup_database()
    
    # We will collect all items into this master list before saving
    all_products_data = []
    
    print("\n--- Step 2 & 3: Scraping and Extracting Data ---")
    for category, url in TARGET_URLS.items():
        print(f"Scraping {category} from: {url}")
        page_soup = scraper.fetch_html(url)
        
        if page_soup:
            product_data = scraper.extract_product_data(page_soup, category)
            if product_data:
                print(f"  -> Extracted {len(product_data)} {category}.")
                # .extend() adds the new items directly into our master list
                all_products_data.extend(product_data)
            
        # Pauses randomly before requesting the next page
        time.sleep(random.uniform(1.5, 3.5))
        
    if not all_products_data:
        print("\nNo data found across any categories. Exiting pipeline.")
        return
        
    print("\n--- Step 4: Saving to Database ---")
    database.save_to_database(all_products_data)
    
    print("\n--- Step 5: Generating Excel Dashboard ---")
    exporter.export_to_excel()
    
    print("\nPipeline execution completed successfully!")

if __name__ == "__main__":
    main()