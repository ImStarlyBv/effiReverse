"""
Location Routes
"""

from flask import Blueprint
from controllers.location_controller import LocationController

location_bp = Blueprint('locations', __name__)

# GET /locations/provinces - List all provinces
location_bp.route('/provinces', methods=['GET'])(LocationController.get_provinces)

# GET /locations/cities?provincia_id=X - List cities for a province
location_bp.route('/cities', methods=['GET'])(LocationController.get_cities)
