
import sys
import os
import json
from bs4 import BeautifulSoup

# Add current directory to path
sys.path.append(os.getcwd())

from services.session_service import session_service

def debug_products():
    print("Fetching products...")
    response = session_service.make_request("/app/articulo", {}, method="GET")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    rows_data = []
    
    # Let's find a row. Usually products are in a table row <tr>
    rows = soup.find_all('tr')
    
    for i, row in enumerate(rows):
        mod_link = row.find('a', class_='modificar')
        ver_link = row.find('a', class_='ver-detalles')
        
        if mod_link:
            row_info = {
                "row_index": i,
                "modificar": mod_link.attrs,
                "ver_detalles": ver_link.attrs if ver_link else None
            }
            rows_data.append(row_info)
            if len(rows_data) >= 5: # Just first 5
                break
                
    with open("debug_rows.json", "w", encoding="utf-8") as f:
        json.dump(rows_data, f, indent=2)
    
    print(f"Saved {len(rows_data)} rows to debug_rows.json")

if __name__ == "__main__":
    try:
        debug_products()
    except Exception as e:
        print(f"Error: {e}")
