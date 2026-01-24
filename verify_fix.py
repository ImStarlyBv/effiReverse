
import sys
import os
import json

# Add current directory to path
sys.path.append(os.getcwd())

from services.product_service import product_service

def verify_fix():
    print("Fetching products via service...")
    products = product_service.get_all()
    
    results = {
        "total_products": len(products),
        "products_with_photo": len([p for p in products if p.get('url_foto')]),
        "sample_products": []
    }
    
    for p in products[:5]:
        results["sample_products"].append({
            "id": p['id'],
            "descripcion": p['descripcion'],
            "url_foto": p.get('url_foto'),
            "image_url": p.get('image_url'),
            "photo_match": p.get('url_foto') == p.get('image_url')
        })
        
    with open("verification_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    
    print(f"Verification results saved to verification_results.json")

if __name__ == "__main__":
    try:
        verify_fix()
    except Exception as e:
        print(f"Error during verification: {e}")
