import sqlite3
import pandas as pd
from api_enricher import get_exchange_rates
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment

DB_NAME = "hardware_prices.db"

def export_to_excel():
    print("Connecting to database for export...")
    
    # Query targets the master 'products' table and pulls the new category column
    conn = sqlite3.connect(DB_NAME)
    query = "SELECT category, title, price, last_updated FROM products"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if df.empty:
        print("No data found in the database to export.")
        return

    print("Fetching live currency rates...")
    rates = get_exchange_rates("USD")
    
    if rates:
        df['price'] = df['price'].str.replace('$', '', regex=False).astype(float)
        df['price_eur'] = (df['price'] * rates['EUR']).round(2)
        df['price_gbp'] = (df['price'] * rates['GBP']).round(2)
        
        # Keep category temporarily so we can sort the sheets
        df = df[['category', 'title', 'price', 'price_eur', 'price_gbp', 'last_updated']]
        
        rename_cols = {
            'title': 'Product Title',
            'price': 'Price (USD)',
            'price_eur': 'Price (EUR)',
            'price_gbp': 'Price (GBP)',
            'last_updated': 'Last Updated'
        }
    else:
        print("Could not fetch live rates. Exporting USD only.")
        return 
    
    filename = "report/international_pricing_report.xlsx"
    print("Generating multi-sheet Excel workbook...")
    
    # Use ExcelWriter to handle multiple sheets
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Find all unique categories in the database
        unique_categories = df['category'].unique()
        
        for cat in unique_categories:
            # Filter the master dataframe for only this specific category
            cat_df = df[df['category'] == cat]
            
            # Drop the category column (since the sheet name makes it obvious)
            cat_df = cat_df.drop(columns=['category'])
            
            # Rename the headers to Title Case for business presentation
            cat_df = cat_df.rename(columns=rename_cols)
            
            # Write to its own distinct sheet
            cat_df.to_excel(writer, sheet_name=cat, index=False)
    
    print("Applying professional formatting to all sheets...")
    format_excel_report(filename)
    
    print(f"Success! Report generated: {filename}")

def format_excel_report(filename):
    """Uses OpenPyXL to format headers, adjust column widths, and apply currency symbols across all sheets."""
    wb = load_workbook(filename)
    
    # Loop through every sheet in the workbook
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        
        header_font = Font(bold=True)
        header_alignment = Alignment(horizontal="center", vertical="center")
        
        for cell in ws[1]:
            cell.font = header_font
            cell.alignment = header_alignment
            
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
            
        # Apply numerical formatting to columns B, C, and D
        for row in range(2, ws.max_row + 1):
            ws[f'B{row}'].number_format = '"$"#,##0.00'
            ws[f'C{row}'].number_format = '"€"#,##0.00'
            ws[f'D{row}'].number_format = '"£"#,##0.00'
            ws[f'E{row}'].alignment = Alignment(horizontal="center")

    wb.save(filename)

if __name__ == "__main__":
    export_to_excel()