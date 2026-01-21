"""
Product Controller
Handles HTTP requests for product operations
"""

from flask import request, jsonify
from services.product_service import product_service


class ProductController:
    
    @staticmethod
    def list_all():
        """GET /products - List all products"""
        try:
            products = product_service.get_all()
            return jsonify({
                "success": True,
                "count": len(products),
                "products": products
            })
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    @staticmethod
    def get_one(product_id):
        """GET /products/<id> - Get single product"""
        try:
            product = product_service.get_by_id(int(product_id))
            if product:
                return jsonify({
                    "success": True,
                    "product": product
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "Product not found"
                }), 404
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    @staticmethod
    def search():
        """GET /products/search?q=X - Search products"""
        try:
            query = request.args.get('q', '')
            if not query:
                return jsonify({
                    "success": False,
                    "error": "Query parameter 'q' is required"
                }), 400
            
            products = product_service.search(query)
            return jsonify({
                "success": True,
                "query": query,
                "count": len(products),
                "products": products
            })
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
