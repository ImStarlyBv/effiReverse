"""
Order Service
Handles remision (order) operations
"""

import time
import random
from datetime import date
from services.session_service import session_service
from services.customer_service import customer_service
from config import ENDPOINTS, EMAIL, DEFAULT_CONVENIO_DROPSHIPPING, DEFAULT_SESSION_EMPRESA


class OrderService:
    
    def create_remision(
        self,
        cliente_id: int,
        direccion_cliente: int,
        items: list,
        sucursal: int = 1,
        bodega: int = 1,
        centro_costos: int = 1,
        fecha_entrega: str = None,
        forma_pago: int = 2
    ) -> dict:
        """Create a remision (order)"""
        
        if fecha_entrega is None:
            fecha_entrega = date.today().strftime("%Y-%m-%d")
        
        # Calculate total
        total = 0
        for item in items:
            precio = float(str(item.get("precio", "0")).replace(",", ""))
            cantidad = int(item.get("cantidad", 1))
            total += precio * cantidad
        
        total_fmt = f"{total:,.0f}"
        
        # Build payload as list of tuples (for duplicate keys)
        payload = [
            ("sucursal", sucursal),
            ("bodega", bodega),
            ("centro_costos", centro_costos),
            ("fecha_entrega", fecha_entrega),
            ("divisa", "DOP"),
            ("trm", 1),
            ("cliente", cliente_id),
            ("direccion_cliente", direccion_cliente),
            ("vendedor", "default"),
            ("tercero", ""),
            ("descuento_global", "0.00"),
            ("convenio_dropshipping", DEFAULT_CONVENIO_DROPSHIPPING),
        ]
        
        # Add items
        for item in items:
            concept_id = f"1{int(time.time() * 1000)}{random.randint(10000000, 99999999)}"[:21]
            precio = str(item.get("precio", "0"))
            
            payload.extend([
                ("id_concepto[]", concept_id),
                ("alquiler[]", item.get("alquiler", 3)),
                ("articulo[]", item.get("articulo_id", "")),
                ("descripcion[]", item.get("descripcion", "")),
                ("observacion_concepto[]", ""),
                ("lote[]", ""),
                ("serie[]", ""),
                ("gift[]", 0),
                ("cantidad[]", item.get("cantidad", 1)),
                ("precio[]", precio),
                ("bruto[]", precio),
                ("descuento[]", 0),
                (f"impuestos[{concept_id}][]", item.get("impuesto_id", 3)),
                ("total_concepto[]", precio),
            ])
        
        # Totals and payment
        payload.extend([
            ("garantia", ""),
            ("observacion", ""),
            ("retencion[]", "default"),
            ("base_retencion[]", 0),
            ("valor_retencion[]", 0),
            ("bruto_transaccion", total_fmt),
            ("total_descuento", 0),
            ("subtotal_transaccion", total_fmt),
            ("propina", 0),
            ("total_impuesto", 0),
            ("total_retencion", 0),
            ("total_transaccion", total_fmt),
            ("prontopago", ""),
            ("fecha_prontopago", ""),
            ("t_forma_pago[]", forma_pago),
            ("valor_forma_pago[]", total_fmt),
            ("total_contado", 0),
            ("recibido", 0),
            ("cambio", 0),
            ("medio_pago[]", "default"),
            ("caja_medio_pago[]", "default"),
            ("cuenta_medio_pago[]", "default"),
            ("valor_medio_pago[]", 0),
            ("observacion_medio_pago[]", ""),
            ("action", 1),
            ("sucursal_cotizacion", ""),
            ("id_cotizacion", ""),
            ("json_ref", ""),
            ("session_empresa", DEFAULT_SESSION_EMPRESA),
            ("session_usuario", EMAIL),
        ])
        
        response = session_service.make_request(ENDPOINTS["create_remision"], payload)
        
        return {
            "success": response.status_code == 200,
            "response": response.text
        }
    
    def create_full_order(
        self,
        dni_number: str,
        nombre: str,
        email: str,
        telefono: str,
        items: list,
        create_customer_if_new: bool = True
    ) -> dict:
        """
        Complete flow: find/create customer, get address, create order
        """
        
        # 1. Search for existing customer
        customer = customer_service.get_by_phone(telefono)
        
        if customer:
            cliente_id = customer['id']
        elif create_customer_if_new:
            # 2. Create new customer
            result = customer_service.create(
                dni_number=dni_number,
                nombre=nombre,
                email=email,
                telefono=telefono
            )
            
            if not result['success']:
                return {
                    "success": False, 
                    "error": "Failed to create customer", 
                    "details": result
                }
            
            # Search again to get ID
            customer = customer_service.get_by_phone(telefono)
            if not customer:
                return {"success": False, "error": "Customer created but not found"}
            
            cliente_id = customer['id']
        else:
            return {"success": False, "error": "Customer not found"}
        
        # 3. Get address
        direccion_id = customer_service.get_first_address_id(cliente_id)
        
        if not direccion_id:
            return {"success": False, "error": "No address found for customer"}
        
        # 4. Create remision
        result = self.create_remision(
            cliente_id=cliente_id,
            direccion_cliente=direccion_id,
            items=items
        )
        
        return {
            "success": result['success'],
            "cliente_id": cliente_id,
            "direccion_id": direccion_id,
            "customer_name": customer['nombre'] if customer else nombre,
            "response": result['response']
        }


# Singleton instance
order_service = OrderService()
