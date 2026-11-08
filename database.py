import sqlite3
from datetime import datetime

DB_NAME = "hardware_prices.db"

def setup_database():
    """Creates the unified products table with a composite unique key."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Drop the old table so we can recreate it with the new rules
    cursor.execute("DROP TABLE IF EXISTS products")
    
    # Create the new master table with a Composite Key
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            title TEXT NOT NULL,
            price TEXT NOT NULL,
            last_updated TEXT NOT NULL,
            UNIQUE(title, price)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database setup complete. Master 'products' table is ready.")

def save_to_database(products_data):
    """Saves products, using title+price as the unique identifier."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for item in products_data:
        # If both title AND price are identical, it just updates the timestamp
        cursor.execute('''
            INSERT INTO products (category, title, price, last_updated)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(title, price) 
            DO UPDATE SET 
                last_updated = excluded.last_updated
        ''', (item['category'], item['title'], item['price'], current_time))
        
    conn.commit()
    conn.close()
    print(f"Successfully saved/updated {len(products_data)} records in the database.")

if __name__ == "__main__":
    setup_database()