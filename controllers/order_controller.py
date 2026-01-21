"""
Order Controller
Handles HTTP requests for order operations
"""

from flask import request, jsonify
from services.order_service import order_service


class OrderController:
    
    @staticmethod
    def create():
        """POST /orders - Create order (remision)"""
        try:
            data = request.json
            
            # Validate required fields
            required = ['cliente_id', 'direccion_cliente', 'items']
            missing = [f for f in required if not data.get(f)]
            if missing:
                return jsonify({
                    "success": False,
                    "error": f"Missing required fields: {', '.join(missing)}"
                }), 400
            
            if not data['items'] or len(data['items']) == 0:
                return jsonify({
                    "success": False,
                    "error": "At least one item is required"
                }), 400
            
            result = order_service.create_remision(
                cliente_id=int(data['cliente_id']),
                direccion_cliente=int(data['direccion_cliente']),
                items=data['items'],
                sucursal=data.get('sucursal', 1),
                bodega=data.get('bodega', 1),
                centro_costos=data.get('centro_costos', 1),
                fecha_entrega=data.get('fecha_entrega'),
                forma_pago=data.get('forma_pago', 2)
            )
            
            if result['success']:
                return jsonify({
                    "success": True,
                    "message": "Order created"
                }), 201
            else:
                return jsonify({
                    "success": False,
                    "error": "Failed to create order",
                    "details": result['response']
                }), 400
                
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    @staticmethod
    def create_full():
        """POST /orders/full - Full flow: create customer + order"""
        try:
            data = request.json
            
            # Validate required fields
            required = ['dni_number', 'nombre', 'email', 'telefono', 'items']
            missing = [f for f in required if not data.get(f)]
            if missing:
                return jsonify({
                    "success": False,
                    "error": f"Missing required fields: {', '.join(missing)}"
                }), 400
            
            if not data['items'] or len(data['items']) == 0:
                return jsonify({
                    "success": False,
                    "error": "At least one item is required"
                }), 400
            
            result = order_service.create_full_order(
                dni_number=data['dni_number'],
                nombre=data['nombre'],
                email=data['email'],
                telefono=data['telefono'],
                items=data['items'],
                create_customer_if_new=data.get('create_customer_if_new', True)
            )
            
            if result['success']:
                return jsonify({
                    "success": True,
                    "message": "Order created successfully",
                    "cliente_id": result['cliente_id'],
                    "direccion_id": result['direccion_id'],
                    "customer_name": result['customer_name']
                }), 201
            else:
                return jsonify({
                    "success": False,
                    "error": result.get('error', 'Unknown error'),
                    "details": result.get('details')
                }), 400
                
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
