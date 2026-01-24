"""
Location Service
Handles fetching provinces and cities from Effi
"""

from bs4 import BeautifulSoup
from services.session_service import session_service
from config import ENDPOINTS


class LocationService:
    
    def get_provinces(self, pais_id: int = 61) -> list:
        """Get provinces for a country (default 61 - Dominican Republic)"""
        payload = {"pais": pais_id}
        response = session_service.make_request(ENDPOINTS["get_provinces"], payload, method="POST")
        
        provinces = []
        soup = BeautifulSoup(response.text, 'html.parser')
        options = soup.find_all('option')
        
        for opt in options:
            value = opt.get('value', '')
            if value and value != 'default':
                text = opt.get_text(strip=True)
                provinces.append({
                    "id": value,
                    "nombre": text
                })
                
        return provinces

    def get_cities(self, provincia_id: int) -> list:
        """Get cities for a province"""
        payload = {"provincia": provincia_id}
        response = session_service.make_request(ENDPOINTS["get_cities"], payload, method="POST")
        
        cities = []
        soup = BeautifulSoup(response.text, 'html.parser')
        options = soup.find_all('option')
        
        for opt in options:
            value = opt.get('value', '')
            if value and value != 'default':
                text = opt.get_text(strip=True)
                cities.append({
                    "id": value,
                    "nombre": text
                })
                
        return cities


# Singleton instance
location_service = LocationService()
