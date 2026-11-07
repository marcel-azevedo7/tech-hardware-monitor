import sqlite3
import pandas as pd
from api_enricher import get_exchange_rates
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment

DB_NAME = "hardware_prices.db"

def export_to_excel():
    print("Connecting to database for export...")
    
    conn = sqlite3.connect(DB_NAME)
    query = "SELECT title, price, last_updated FROM laptops"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if df.empty:
        print("No data found in the database to export.")
        return

    print("Fetching live currency rates...")
    rates = get_exchange_rates("USD")
    
    if rates:
        # Permanently convert the original string column into a float
        df['price'] = df['price'].str.replace('$', '', regex=False).astype(float)
        
        # Calculate new columns using the clean float
        df['price_eur'] = (df['price'] * rates['EUR']).round(2)
        df['price_gbp'] = (df['price'] * rates['GBP']).round(2)
        
        df = df[['title', 'price', 'price_eur', 'price_gbp', 'last_updated']]
        
        # Rename columns for the final business presentation
        df = df.rename(columns={
            'title': 'Product Title',
            'price': 'Price (USD)',
            'price_eur': 'Price (EUR)',
            'price_gbp': 'Price (GBP)',
            'last_updated': 'Last Updated'
        })
    else:
        print("Could not fetch live rates. Exporting USD only.")
    
    # Export raw data to the report folder
    filename = "report/international_pricing_report.xlsx"
    df.to_excel(filename, index=False, engine='openpyxl')
    
    print("Applying professional formatting to the report...")
    format_excel_report(filename)
    
    print(f"Success! Report generated: {filename}")

def format_excel_report(filename):
    """Uses OpenPyXL to format headers, adjust column widths, and apply currency symbols."""
    wb = load_workbook(filename)
    ws = wb.active
    
    # Format the Header Row (Bold & Centered)
    header_font = Font(bold=True)
    header_alignment = Alignment(horizontal="center", vertical="center")
    
    for cell in ws[1]:
        cell.font = header_font
        cell.alignment = header_alignment
        
    # Auto-adjust column widths based on string length
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        
        ws.column_dimensions[column_letter].width = max_length + 2
        
    # Apply Currency Number Formats to all three pricing columns (B, C, and D)
    for row in range(2, ws.max_row + 1):
        ws[f'B{row}'].number_format = '"$"#,##0.00'
        ws[f'C{row}'].number_format = '"€"#,##0.00'
        ws[f'D{row}'].number_format = '"£"#,##0.00'
        
        # Center align the timestamp
        ws[f'E{row}'].alignment = Alignment(horizontal="center")

    wb.save(filename)

if __name__ == "__main__":
    export_to_excel()