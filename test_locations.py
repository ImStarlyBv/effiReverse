
import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from services.location_service import location_service

def test_locations():
    print("Testing LocationService (Both using POST)...")
    
    # Test Provinces
    print("\nFetching provinces (Country 61 - DR)...")
    provinces = location_service.get_provinces(61)
    print(f"Count: {len(provinces)}")
    
    if provinces:
        print("First 3 provinces:")
        for p in provinces[:3]:
            print(f"  - {p['id']}: {p['nombre']}")
            
        sd_id = next((p['id'] for p in provinces if "Santo Domingo" in p['nombre']), None)
        if sd_id:
            # Test Cities
            print(f"\nFetching cities for province {sd_id} using POST...")
            cities = location_service.get_cities(int(sd_id))
            print(f"Count: {len(cities)}")
            if cities:
                print("First 3 cities:")
                for c in cities[:3]:
                    print(f"  - {c['id']}: {c['nombre']}")
            else:
                print("FAILURE: No cities found for Santo Domingo with POST")
        else:
            print("WARNING: Santo Domingo not found")
    else:
        print("FAILURE: No provinces found with POST")

if __name__ == "__main__":
    test_locations()
