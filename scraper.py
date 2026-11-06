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

def extract_laptop_data(soup):
    """Finds all laptop containers and extracts the title and price from each."""
    # 1. Find all the parent wrapper containers on the page
    containers = soup.find_all("div", class_="thumbnail")
    print(f"Found {len(containers)} laptops on this page.\n")
    
    laptops = []
    
    # 2. Loop through each container to extract the specific details
    for container in containers:
        # Find the price tag using the exact tag and class you discovered
        price_tag = container.find("h4", class_="price")
        # Extract the text and remove any accidental blank spaces
        price = price_tag.text.strip() if price_tag else "No Price"
        
        # Find the title tag
        title_tag = container.find("a", class_="title")
        # The 'title' attribute often holds the full un-truncated name
        title = title_tag.get("title") if title_tag else "No Title"
        
        print(f"{title}: {price}")
        laptops.append({"title": title, "price": price})
        
    return laptops

if __name__ == "__main__":
    target_url = "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops"
    
    print(f"Fetching data from: {target_url}...")
    page_soup = fetch_html(target_url)
    
    if page_soup:
        # Pass the downloaded HTML to our new extraction function
        laptop_data = extract_laptop_data(page_soup)