"""
Customer Controller
Handles HTTP requests for customer operations
"""

from flask import request, jsonify
from services.customer_service import customer_service


class CustomerController:
    
    @staticmethod
    def list_all():
        """GET /customers - List all customers"""
        try:
            customers = customer_service.search()
            return jsonify({
                "success": True,
                "count": len(customers),
                "customers": customers
            })
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    @staticmethod
    def search():
        """GET /customers/search?phone=X&nombre=Y"""
        try:
            phone = request.args.get('phone', '')
            nombre = request.args.get('nombre', '')
            id = request.args.get('id', '')
            
            customers = customer_service.search(id=id, nombre=nombre, telefono=phone)
            return jsonify({
                "success": True,
                "count": len(customers),
                "customers": customers
            })
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    @staticmethod
    def create():
        """POST /customers - Create new customer"""
        try:
            data = request.json
            
            # Validate required fields
            required = ['dni_number', 'nombre', 'email', 'telefono']
            missing = [f for f in required if not data.get(f)]
            if missing:
                return jsonify({
                    "success": False, 
                    "error": f"Missing required fields: {', '.join(missing)}"
                }), 400
            
            result = customer_service.create(
                dni_number=data['dni_number'],
                nombre=data['nombre'],
                email=data['email'],
                telefono=data['telefono'],
                whatsapp=data.get('whatsapp'),
                dni_type=data.get('dni_type', 21),
                pais=data.get('pais', 61),
                provincia=data.get('provincia', 981),
                ciudad=data.get('ciudad', 62304),
                direccion=data.get('direccion', '91000'),
                genero=data.get('genero', 'M')
            )
            
            if result['success']:
                # Get the created customer
                customer = customer_service.get_by_phone(data['telefono'])
                return jsonify({
                    "success": True,
                    "message": "Customer created",
                    "customer": customer
                }), 201
            else:
                return jsonify({
                    "success": False,
                    "error": "Failed to create customer",
                    "details": result['response']
                }), 400
                
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    @staticmethod
    def get_addresses(customer_id):
        """GET /customers/<id>/addresses"""
        try:
            addresses = customer_service.get_addresses(int(customer_id))
            return jsonify({
                "success": True,
                "customer_id": customer_id,
                "count": len(addresses),
                "addresses": addresses
            })
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
