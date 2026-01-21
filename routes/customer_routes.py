"""
Customer Routes
"""

from flask import Blueprint
from controllers.customer_controller import CustomerController

customer_bp = Blueprint('customers', __name__)

# GET /customers - List all
customer_bp.route('', methods=['GET'])(CustomerController.list_all)

# GET /customers/search?phone=X&nombre=Y
customer_bp.route('/search', methods=['GET'])(CustomerController.search)

# POST /customers - Create
customer_bp.route('', methods=['POST'])(CustomerController.create)

# GET /customers/<id>/addresses
customer_bp.route('/<customer_id>/addresses', methods=['GET'])(CustomerController.get_addresses)
