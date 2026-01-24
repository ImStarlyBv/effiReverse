"""
Location Controller
Handles HTTP requests for location operations
"""

from flask import request, jsonify
from services.location_service import location_service


class LocationController:
    
    @staticmethod
    def get_provinces():
        """GET /locations/provinces - Get all provinces"""
        try:
            pais_id = request.args.get('pais_id', 61)
            provinces = location_service.get_provinces(pais_id)
            return jsonify({
                "success": True,
                "count": len(provinces),
                "provinces": provinces
            })
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    @staticmethod
    def get_cities():
        """GET /locations/cities - Get cities for a province"""
        try:
            provincia_id = request.args.get('provincia_id')
            if not provincia_id:
                return jsonify({
                    "success": False,
                    "error": "Query parameter 'provincia_id' is required"
                }), 400
                
            cities = location_service.get_cities(provincia_id)
            return jsonify({
                "success": True,
                "count": len(cities),
                "cities": cities
            })
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
