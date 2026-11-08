import requests
from bs4 import BeautifulSoup

def fetch_html(url):
    """Sends an HTTP GET request and returns a parsed BeautifulSoup object."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

def extract_product_data(soup, category):
    """Finds all product containers and extracts the category, title, and price."""
    containers = soup.find_all("div", class_="thumbnail")
    
    products = []
    
    for container in containers:
        price_tag = container.find("h4", class_="price")
        price = price_tag.text.strip() if price_tag else "No Price"
        
        title_tag = container.find("a", class_="title")
        title = title_tag.get("title") if title_tag else "No Title"
        
        # We now tag each dictionary with its specific category
        products.append({
            "category": category,
            "title": title, 
            "price": price
        })
        
    return products

if __name__ == "__main__":
    # Test with just laptops to ensure our new category tag works
    target_url = "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops"
    
    print(f"Fetching data from: {target_url}...")
    page_soup = fetch_html(target_url)
    
    if page_soup:
        # We pass the category 'Laptops' so the scraper knows what it is extracting
        product_data = extract_product_data(page_soup, "Laptops")
        if product_data:
            print(f"Extracted {len(product_data)} items.")
            print(f"Example of new data structure: {product_data[0]}")