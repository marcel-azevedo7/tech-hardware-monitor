import sqlite3
from datetime import datetime

DB_NAME = "hardware_prices.db"

def setup_database():
    """Creates the database and the laptops table if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # The UNIQUE constraint on 'title' is what triggers our UPSERT logic
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS laptops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            price TEXT NOT NULL,
            last_updated TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database setup complete.")

def save_to_database(laptops_data):
    """Saves new laptops or updates existing ones using UPSERT."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Generate a standard timestamp for when the script runs
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for laptop in laptops_data:
        # The '?' placeholders protect against SQL Injection
        # 'excluded.price' grabs the new price that caused the conflict
        cursor.execute('''
            INSERT INTO laptops (title, price, last_updated)
            VALUES (?, ?, ?)
            ON CONFLICT(title) 
            DO UPDATE SET 
                price = excluded.price,
                last_updated = excluded.last_updated
        ''', (laptop['title'], laptop['price'], current_time))
        
    conn.commit()
    conn.close()
    print(f"Successfully saved/updated {len(laptops_data)} records in the database.")

# Quick test block to ensure table creation works
if __name__ == "__main__":
    setup_database()