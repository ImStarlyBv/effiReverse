"""
Product Service
Handles product/article operations
"""

from bs4 import BeautifulSoup
from services.session_service import session_service


class ProductService:
    
    def get_all(self) -> list:
        """Get all products/articles"""
        response = session_service.make_request("/app/articulo", {}, method="GET")
        return self._parse_products(response.text)
    
    def get_by_id(self, product_id: int) -> dict:
        """Get a specific product by ID"""
        products = self.get_all()
        for product in products:
            if product['id'] == product_id:
                return product
        return None
    
    def search(self, query: str) -> list:
        """Search products by name/description"""
        products = self.get_all()
        query_lower = query.lower()
        return [p for p in products if query_lower in p['descripcion'].lower()]
    
    def _parse_products(self, html: str) -> list:
        """Parse HTML response and extract product data"""
        products = []
        soup = BeautifulSoup(html, 'html.parser')
        
        # Products are in table rows <tr>
        rows = soup.find_all('tr')
        
        for row in rows:
            # Look for a row that has a 'modificar' link (primary source of data)
            link = row.find('a', class_='modificar')
            # Look for 'ver-detalles' link (secondary source, often contains url_foto)
            ver_detalles_link = row.find('a', class_='ver-detalles')
            
            if not link:
                continue
                
            try:
                product = {
                    "id": int(link.get('data-id', 0)),
                    "codigo": link.get('data-codigo', ''),
                    "descripcion": link.get('data-descripcion', ''),
                    "referencia": link.get('data-referencia', ''),
                    "t_articulo": link.get('data-t_articulo', ''),
                    "categoria": link.get('data-categoria', ''),
                    "sucursal": link.get('data-sucursal', ''),
                    "marca": link.get('data-marca', ''),
                    
                    # Pricing
                    "p_costo": link.get('data-p_costo', '0'),
                    "p_costo_promedio": link.get('data-p_costo_promedio', '0'),
                    "p_min_venta": link.get('data-p_min_venta', '0'),
                    
                    # Stock
                    "gestion_stock": link.get('data-gestion_stock', '0'),
                    "stock_minimo": link.get('data-stock_minimo', '0'),
                    "stock_optimo": link.get('data-stock_optimo', '0'),
                    
                    # Flags
                    "compras": link.get('data-compras', '0') == '1',
                    "ventas": link.get('data-ventas', '0') == '1',
                    "dropshipping": link.get('data-dropshipping', '0') == '1',
                    "alquiler": link.get('data-alquiler', '0') == '1',
                    
                    # Discount
                    "descuento": link.get('data-descuento', '0'),
                    "descuento_max": link.get('data-descuento_max', ''),
                    
                    # Tax
                    "json_impuestos": link.get('data-json_impuestos', '[]'),
                    
                    # Media - initially from 'modificar'
                    "url_foto": link.get('data-url_foto', ''),
                    "url_video": link.get('data-url_video', ''),
                    "descripcion_detallada": link.get('data-descripcion_detallada', ''),
                }
                
                # If url_foto is empty or missing, try to get it from 'ver-detalles' link
                if (not product["url_foto"] or product["url_foto"] == "") and ver_detalles_link:
                    product["url_foto"] = ver_detalles_link.get('data-url_foto', '')
                
                # Double check for image_url alias
                product["image_url"] = product["url_foto"]
                
                products.append(product)
                
            except Exception as e:
                print(f"Error parsing product: {e}")
                continue
        
        return products


# Singleton instance
product_service = ProductService()
