"""
Product Routes
"""

from flask import Blueprint
from controllers.product_controller import ProductController

product_bp = Blueprint('products', __name__)

# GET /products - List all
product_bp.route('', methods=['GET'])(ProductController.list_all)

# GET /products/search?q=X - Search
product_bp.route('/search', methods=['GET'])(ProductController.search)

# GET /products/<id> - Get one
product_bp.route('/<product_id>', methods=['GET'])(ProductController.get_one)
