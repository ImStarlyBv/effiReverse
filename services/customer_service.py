"""
Customer Service
Handles customer CRUD operations
"""

from bs4 import BeautifulSoup
from services.session_service import session_service
from config import ENDPOINTS, EMAIL


class CustomerService:
    
    def create(
        self,
        dni_number: str,
        nombre: str,
        email: str,
        telefono: str,
        whatsapp: str = None,
        dni_type: int = 21,
        pais: int = 61,
        provincia: int = 981,
        ciudad: int = 62304,
        direccion: str = "91000",
        genero: str = "M"
    ) -> dict:
        """Create a new customer"""
        
        if whatsapp is None:
            whatsapp = telefono
        
        payload = {
            "t_dni": dni_type,
            "numero": dni_number,
            "nombre": nombre,
            "email": email,
            "web": "",
            "pais[]": pais,
            "provincia[]": provincia,
            "ciudad[]": ciudad,
            "direccion[]": direccion,
            "ref_direccion[]": direccion,
            "latitud[]": "",
            "longitud[]": "",
            "telefono1": telefono,
            "ref_telefono1": "",
            "telefono2": "",
            "ref_telefono2": "",
            "celular": "",
            "whatsapp": whatsapp,
            "fecha_nacimiento": "2000-01-01",
            "genero": genero,
            "est_civil": 1,
            "limite_total": "",
            "cupo_credito": "",
            "facetime": "",
            "skype": "",
            "t_persona": 1,
            "t_regimen_iva": 6,
            "t_cliente": 1,
            "divisa": "DOP",
            "t_precio": 1,
            "ciiu": "default",
            "t_forma_pago": 2,
            "retencion": "default",
            "permitir_venta": 1,
            "descuento": "",
            "t_marketing": "default",
            "sucursal": "default",
            "responsable_asignado": EMAIL,
            "vendedor": "default",
            "observacion": "",
            "codigo": ""
        }
        
        response = session_service.make_request(ENDPOINTS["create_customer"], payload)
        
        return {
            "success": response.status_code == 200,
            "response": response.text
        }
    
    def search(self, id: str = "", nombre: str = "", telefono: str = "") -> list:
        """Search customers"""
        payload = {
            "id": id,
            "nombre": nombre,
            "celular_whatsapp": telefono
        }
        
        response = session_service.make_request(ENDPOINTS["search_customers"], payload)
        
        customers = []
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.find_all('tr', attrs={'data-codigo': True})
        
        for row in rows:
            cells = row.find_all('td')
            customers.append({
                "id": int(row.get('data-codigo')),
                "nombre": row.get('data-nombre'),
                "t_precio": row.get('data-t_precio'),
                "t_forma_pago": row.get('data-t_forma_pago'),
                "documento": cells[0].get_text(strip=True) if len(cells) > 0 else "",
                "telefono": cells[2].get_text(strip=True) if len(cells) > 2 else ""
            })
        
        return customers
    
    def get_by_phone(self, phone: str) -> dict:
        """Get customer by phone number"""
        customers = self.search(telefono=phone)
        return customers[0] if customers else None
    
    def get_by_id(self, customer_id: int) -> dict:
        """Get customer by ID"""
        customers = self.search(id=str(customer_id))
        return customers[0] if customers else None
    
    def get_addresses(self, cliente_id: int) -> list:
        """Get addresses for a customer"""
        payload = {"tercero": cliente_id}
        response = session_service.make_request(ENDPOINTS["get_addresses"], payload)
        
        addresses = []
        soup = BeautifulSoup(response.text, 'html.parser')
        options = soup.find_all('option')
        
        for opt in options:
            value = opt.get('value', '')
            if value:
                addresses.append({
                    "id": int(value),
                    "direccion": opt.get_text(strip=True)
                })
        
        return addresses
    
    def get_first_address_id(self, cliente_id: int) -> int:
        """Get first address ID for a customer"""
        addresses = self.get_addresses(cliente_id)
        return addresses[0]["id"] if addresses else None


# Singleton instance
customer_service = CustomerService()
