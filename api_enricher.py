import requests

def get_exchange_rates(base_currency="USD"):
    """
    Connects to a public REST API to fetch live currency exchange rates.
    Returns a dictionary with the target conversion rates.
    """
    # This open endpoint provides daily updated rates relative to a base currency
    url = f"https://open.er-api.com/v6/latest/{base_currency}"
    
    try:
        # Send the GET request to the API
        response = requests.get(url)
        response.raise_for_status()
        
        # Convert the JSON response directly into a Python dictionary
        data = response.json()
        
        # The API returns a large dictionary. The actual currencies are nested 
        # inside a key called 'rates'. We extract just that dictionary.
        rates = data.get("rates", {})
        
        # We isolate only the European markets for our specific pipeline
        target_rates = {
            "EUR": rates.get("EUR"),
            "GBP": rates.get("GBP")
        }
        
        return target_rates
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching API data: {e}")
        return None

# Quick test block to ensure we can connect to the API
if __name__ == "__main__":
    print("Testing Live API Connection...")
    live_rates = get_exchange_rates("USD")
    
    if live_rates:
        print(f"Success! Current Rates:")
        print(f"1 USD = {live_rates['EUR']} EUR")
        print(f"1 USD = {live_rates['GBP']} GBP")